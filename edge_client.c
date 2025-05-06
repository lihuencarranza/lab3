// edge_client.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SENSOR_IP "127.0.0.1"
#define SENSOR_PORT 5000

#define ACTUATOR_IP "127.0.0.1"
#define ACTUATOR_PORT 5001

#include <pthread.h>
#define SERVICE_REG_PORT 6000

#define MAX_SERVICES 10

char service_list[MAX_SERVICES][256];
int service_count = 0;
pthread_mutex_t lock;

void *service_server_thread(void *arg) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);
    char buffer[256];

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(SERVICE_REG_PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 5);

    printf("Edge service registration server listening on port %d...\n", SERVICE_REG_PORT);

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen);
        if (new_socket >= 0) {
            memset(buffer, 0, sizeof(buffer));
            read(new_socket, buffer, sizeof(buffer));
            
            pthread_mutex_lock(&lock);
            if (service_count < MAX_SERVICES) {
                strncpy(service_list[service_count++], buffer, 255);
                printf("Registered service: %s\n", buffer);
            }
            pthread_mutex_unlock(&lock);

            close(new_socket);
        }
    }

    return NULL;
}


int read_humidity() {
    int sock;
    struct sockaddr_in address;
    int humidity = -1;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_port = htons(SENSOR_PORT);
    inet_pton(AF_INET, SENSOR_IP, &address.sin_addr);

    if (connect(sock, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Error connecting to sensor");
        return -1;
    }

    recv(sock, &humidity, sizeof(humidity), 0);
    close(sock);
    return humidity;
}

void send_led_command(const char *cmd) {
    int sock;
    struct sockaddr_in address;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_port = htons(ACTUATOR_PORT);
    inet_pton(AF_INET, ACTUATOR_IP, &address.sin_addr);

    if (connect(sock, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Error connecting to actuator");
        return;
    }

    send(sock, cmd, strlen(cmd), 0);
    close(sock);
}

int main() {
    pthread_mutex_init(&lock, NULL);
    pthread_t tid;
    pthread_create(&tid, NULL, service_server_thread, NULL);

    while (1) {
        int humidity = read_humidity();
        if (humidity < 0) {
            sleep(1);
            continue;
        }

        float voltage = humidity * 3.3 / 1023.0;
        printf("Humidity (ADC): %d - Voltage: %.2f V\n", humidity, voltage);

        if (humidity < 30) {
            printf("Humidity < 30 => Sending ON command to LED\n");
            send_led_command("ON");
        } else {
            printf("Humidity >= 30 => Sending OFF command to LED\n");
            send_led_command("OFF");
        }

        sleep(5);
    }

    return 0;
}
