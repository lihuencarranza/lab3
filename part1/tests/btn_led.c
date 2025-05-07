#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

#define CHIP_NAME "gpiochip0"
#define GPIO_LED 26
#define GPIO_BTN 19

int main() {
    struct gpiod_chip *chip;
    struct gpiod_line *led_line;
    struct gpiod_line *btn_line;

    // Open GPIO chip
    chip = gpiod_chip_open_by_name(CHIP_NAME);
    if (!chip) {
        perror("gpiod_chip_open_by_name");
        return 1;
    }

    // Get lines
    led_line = gpiod_chip_get_line(chip, GPIO_LED);
    btn_line = gpiod_chip_get_line(chip, GPIO_BTN);
    if (!led_line || !btn_line) {
        perror("gpiod_chip_get_line");
        gpiod_chip_close(chip);
        return 1;
    }

    // Configure LED as output
    if (gpiod_line_request_output(led_line, "test_led", 0) < 0) {
        perror("gpiod_line_request_output");
        gpiod_chip_close(chip);
        return 1;
    }

    // Configure button as input (no internal resistors)
    if (gpiod_line_request_input(btn_line, "test_button") < 0) {
        perror("gpiod_line_request_input");
        gpiod_chip_close(chip);
        return 1;
    }

    printf("Press the button to turn on the LED (Ctrl+C to exit)...\n");

    int prev = -1;

    while (1) {
        int btn_value = gpiod_line_get_value(btn_line);
        if (btn_value < 0) {
            perror("gpiod_line_get_value");
            break;
        }

        if (btn_value != prev) {
            gpiod_line_set_value(led_line, btn_value);
            printf("Button: %d | LED: %s\n", btn_value, btn_value ? "ON" : "OFF");
            prev = btn_value;
        }

        usleep(100000);  // 100 ms
    }

    gpiod_chip_close(chip);
    return 0;
}
