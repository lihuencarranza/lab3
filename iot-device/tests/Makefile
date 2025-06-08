# Makefile for compiling and executing GPIO test programs

CC = gcc
CFLAGS = -o
SRC = test_led.c test_button.c btn_led.c test_humidity.c
EXEC = test_led test_button btn_led test_humidity

all: $(EXEC)

test_led: test_led.c
	$(CC) $(CFLAGS) test_led test_led.c -lgpiod

test_button: test_button.c
	$(CC) $(CFLAGS) test_button test_button.c -lgpiod

btn_led: btn_led.c
	$(CC) $(CFLAGS) btn_led btn_led.c -lgpiod

test_humidity: test_humidity.c
	$(CC) $(CFLAGS) test_humidity test_humidity.c

clean:
	rm -f $(EXEC)