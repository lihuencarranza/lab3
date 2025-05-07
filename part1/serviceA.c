// servicioA.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define SPI_DEVICE "/dev/spidev0.0"
#define SPI_SPEED 1350000
#define PORT 5000

int read_channel(int fd, uint8_t channel) {
    uint8_t tx[] = {1, (8 + channel) << 4, 0};
    uint8_t rx[3] = {0};

    struct spi_ioc_transfer tr = {
        .tx_buf = (unsigned long)tx,
        .rx_buf = (unsigned long)rx,
        .len = 3,
        .speed_hz = SPI_SPEED,
        .bits_per_word = 8,
    };

    if (ioctl(fd, SPI_IOC_MESSAGE(1), &tr) < 1) {
        perror("SPI transfer failed");
        return -1;
    }

    int value = ((rx[1] & 3) << 8) | rx[2];
    return value;
}

#define EDGE_IP "127.0.0.1"
#define EDGE_PORT 6000

void register_service() {
    int sock;
    struct sockaddr_in edge_addr;
    char *message = "RPi-1,Read_Humidity,0,";

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
    int spi_fd = open(SPI_DEVICE, O_RDWR);
    if (spi_fd < 0) {
        perror("Cannot open SPI device");
        return 1;
    }
    register_service();

    uint8_t mode = 0;
    ioctl(spi_fd, SPI_IOC_WR_MODE, &mode);
    uint32_t speed = SPI_SPEED;
    ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);

    int server_fd, new_socket;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);

    printf("Service A waiting for connections...\n");
    register_service();

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen);
        if (new_socket >= 0) {
            int humidity = read_channel(spi_fd, 0);
            printf("Humidity sent: %d\n", humidity);
            send(new_socket, &humidity, sizeof(humidity), 0);
            close(new_socket);
        }
    }

    close(spi_fd);
    return 0;
}
