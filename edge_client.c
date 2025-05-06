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
