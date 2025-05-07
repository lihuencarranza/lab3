// serviceB.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <gpiod.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <pthread.h>

#define GPIO_CHIP "/dev/gpiochip0"
#define GPIO_LED 26
#define GPIO_BUTTON 19
#define PORT 5001

int led_on = 0;
struct gpiod_line *led;
#define EDGE_IP "127.0.0.1"
#define EDGE_PORT 6000

void *button_thread(void *arg) {
    struct gpiod_chip *chip = gpiod_chip_open(GPIO_CHIP);
    struct gpiod_line *button = gpiod_chip_get_line(chip, GPIO_BUTTON);

    gpiod_line_request_input(button, "button");

    while (1) {
        int value = gpiod_line_get_value(button);
        if (value == 1 && led_on) {
            printf("Button pressed => Turning LED OFF\n");
            gpiod_line_set_value(led, 0);
            led_on = 0;
        }
        usleep(100000); // check every 100 ms
    }

    gpiod_chip_close(chip);
    return NULL;
}

void register_service() {
    int sock;
    struct sockaddr_in edge_addr;
    char *message = "RPi-2,Set_LED,1,state";

    sock = socket(AF_INET, SOCK_STREAM, 0);
    edge_addr.sin_family = AF_INET;
    edge_addr.sin_port = htons(EDGE_PORT);
    inet_pton(AF_INET, EDGE_IP, &edge_addr.sin_addr);

    if (connect(sock, (struct sockaddr *)&edge_addr, sizeof(edge_addr)) < 0) {
        perror("Error registering service to edge");
        return;
    }

    send(sock, message, strlen(message), 0);
    close(sock);
}


int main() {
    struct gpiod_chip *chip = gpiod_chip_open(GPIO_CHIP);
    if (!chip) {
        perror("Error opening GPIO chip");
        return 1;
    }

    register_service();

    led = gpiod_chip_get_line(chip, GPIO_LED);
    if (!led || gpiod_line_request_output(led, "led", 0) < 0) {
        perror("Error accessing LED line");
        return 1;
    }

    pthread_t tid;
    pthread_create(&tid, NULL, button_thread, NULL);

    int server_fd, new_socket;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);

    printf("Service B waiting for connections...\n");

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen);
        if (new_socket >= 0) {
            char buffer[10] = {0};
            read(new_socket, buffer, sizeof(buffer));

            if (strcmp(buffer, "ON") == 0) {
                printf("Command received: ON\n");
                gpiod_line_set_value(led, 1);
                led_on = 1;
            } else if (strcmp(buffer, "OFF") == 0) {
                printf("Command received: OFF\n");
                gpiod_line_set_value(led, 0);
                led_on = 0;
            }
            close(new_socket);
        }
    }

    gpiod_chip_close(chip);
    return 0;
}
