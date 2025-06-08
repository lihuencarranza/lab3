#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

#define CHIP_NAME "gpiochip0"
#define GPIO_LINE 19

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

    if (gpiod_line_request_input(line, "test_button") < 0) {
        perror("gpiod_line_request_input");
        gpiod_chip_close(chip);
        return 1;
    }

    printf("Press the button...\n");
    for (int i = 0; i < 20; ++i) {  // reads the state every 200ms for 4 seconds
        int value = gpiod_line_get_value(line);
        if (value < 0) {
            perror("gpiod_line_get_value");
            break;
        }
        printf("State: %d\n", value);
        usleep(200000);  // 200 ms
    }

    gpiod_chip_close(chip);
    return 0;
}
