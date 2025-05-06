#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

#define CHIP_NAME "gpiochip0"
#define GPIO_LINE 26

int main() {
    struct gpiod_chip *chip;
    struct gpiod_line *line;

    chip = gpiod_chip_open_by_name(CHIP_NAME);
    if (!chip) {
        perror("gpiod_chip_open_by_name");
        return 1;
    }

    line = gpiod_chip_get_line(chip, GPIO_LINE);
    if (!line) {
        perror("gpiod_chip_get_line");
        gpiod_chip_close(chip);
        return 1;
    }

    if (gpiod_line_request_output(line, "test_led", 0) < 0) {
        perror("gpiod_line_request_output");
        gpiod_chip_close(chip);
        return 1;
    }

    printf("Turning on LED...\n");
    gpiod_line_set_value(line, 1);
    sleep(2);
    gpiod_line_set_value(line, 0);
    printf("Off.\n");

    gpiod_chip_close(chip);
    return 0;
}
