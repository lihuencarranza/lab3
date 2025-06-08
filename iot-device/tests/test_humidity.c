#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>
#include <string.h>

#define SPI_DEVICE "/dev/spidev0.0"
#define SPI_SPEED 1350000
#define VREF 3.3
#define MCP3008_MAX 1023

int read_channel(int fd, int channel) {
    uint8_t tx[] = {
        0x01,                        // Start bit
        (0x08 | channel) << 4,       // Config byte: single-ended + channel
        0x00                         // Placeholder
    };
    uint8_t rx[3] = {0};

    struct spi_ioc_transfer tr = {
        .tx_buf = (unsigned long)tx,
        .rx_buf = (unsigned long)rx,
        .len = 3,
        .delay_usecs = 0,
        .speed_hz = SPI_SPEED,
        .bits_per_word = 8,
    };

    if (ioctl(fd, SPI_IOC_MESSAGE(1), &tr) < 1) {
        perror("Error en la transferencia SPI");
        return -1;
    }

    int value = ((rx[1] & 0x03) << 8) | rx[2];
    return value;
}

int main() {
    int fd = open(SPI_DEVICE, O_RDWR);
    if (fd < 0) {
        perror("No se pudo abrir el dispositivo SPI");
        return 1;
    }

    uint8_t mode = SPI_MODE_0;
    uint8_t bits = 8;

    ioctl(fd, SPI_IOC_WR_MODE, &mode);
    ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &(uint32_t){SPI_SPEED});

    while (1) {
        int value = read_channel(fd, 0);  // Canal 0
        if (value >= 0) {
            float voltage = value * VREF / MCP3008_MAX;
            printf("Humedad (ADC): %d - Voltaje aproximado: %.2f V\n", value, voltage);
        }
        sleep(1);
    }

    close(fd);
    return 0;
}
