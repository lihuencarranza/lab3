// edge_client.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#define SENSOR_IP "127.0.0.1"
#define SENSOR_PORT 5000

#define ACTUATOR_IP "127.0.0.1"
#define ACTUATOR_PORT 5001

#define SERVICE_REG_PORT 6000
#define COMMAND_PORT 7000

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
void *command_server_thread(void *arg) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    char buffer[256], response[256];
    socklen_t addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(COMMAND_PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 5);

    printf("Edge command server listening on port %d...\n", COMMAND_PORT);

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen);
        if (new_socket >= 0) {
            memset(buffer, 0, sizeof(buffer));
            read(new_socket, buffer, sizeof(buffer));
            printf("Received command: %s\n", buffer);

            memset(response, 0, sizeof(response));

            if (strcmp(buffer, "READ RPi-1 Read_Humidity") == 0) {
                int humidity = read_humidity();
                if (humidity >= 0) {
                    float voltage = humidity * 3.3 / 1023.0;
                    snprintf(response, sizeof(response), "Humidity: %d (%.2f V)", humidity, voltage);
                } else {
                    snprintf(response, sizeof(response), "Failed to read humidity.");
                }
            } else if (strcmp(buffer, "WRITE RPi-2 Set_LED ON") == 0) {
                send_led_command("ON");
                snprintf(response, sizeof(response), "LED turned ON");
            } else if (strcmp(buffer, "WRITE RPi-2 Set_LED OFF") == 0) {
                send_led_command("OFF");
                snprintf(response, sizeof(response), "LED turned OFF");
            } else if (strcmp(buffer, "LIST SERVICES") == 0) {
                pthread_mutex_lock(&lock);
                if (service_count == 0) {
                    snprintf(response, sizeof(response), "No services registered.");
                } else {
                    for (int i = 0; i < service_count; i++) {
                        strcat(response, service_list[i]);
                        strcat(response, "\n");
                    }
                }
                pthread_mutex_unlock(&lock);
            } else if (strcmp(buffer, "HELP") == 0) {
                snprintf(response, sizeof(response),
                    "Available commands:\n"
                    "READ RPi-1 Read_Humidity\n"
                    "WRITE RPi-2 Set_LED ON\n"
                    "WRITE RPi-2 Set_LED OFF\n"
                    "APP HumidCheck\n"
                    "HELP\n");
            } else if (strcmp(buffer, "APP HumidCheck") == 0) {
                int humidity = read_humidity();
                if (humidity >= 0) {
                    float voltage = humidity * 3.3 / 1023.0;
                    char action[32];
            
                    if (humidity < 30) {
                        send_led_command("ON");
                        strcpy(action, "LED turned ON");
                    } else {
                        send_led_command("OFF");
                        strcpy(action, "LED turned OFF");
                    }
            
                    snprintf(response, sizeof(response),
                        "[HumidCheck App]\nHumidity: %d (%.2f V)\nAction: %s\n",
                        humidity, voltage, action);
                } else {
                    snprintf(response, sizeof(response), "Failed to run HumidCheck App (sensor error).");
                }
            }            
            else {
                snprintf(response, sizeof(response), "Unknown command.");
            }

            send(new_socket, response, strlen(response), 0);
            close(new_socket);
        }
    }

    return NULL;
}

int main() {
    pthread_mutex_init(&lock, NULL);
    pthread_t tid1, tid2;
    pthread_create(&tid1, NULL, service_server_thread, NULL);
    pthread_create(&tid2, NULL, command_server_thread, NULL);

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