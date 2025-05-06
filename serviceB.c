// service_B.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <gpiod.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define GPIO_CHIP "/dev/gpiochip0"
#define GPIO_LED 26
#define PORT 5001

int main() {
    struct gpiod_chip *chip = gpiod_chip_open(GPIO_CHIP);
    if (!chip) {
        perror("Error opening GPIO chip");
        return 1;
    }

    struct gpiod_line *led = gpiod_chip_get_line(chip, GPIO_LED);
    if (!led || gpiod_line_request_output(led, "led", 0) < 0) {
        perror("Error accessing LED line");
        return 1;
    }

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
                sleep(2);  // Turn on LED for 2 seconds
                gpiod_line_set_value(led, 0);
            }
            close(new_socket);
        }
    }

    gpiod_chip_close(chip);
    return 0;
}
