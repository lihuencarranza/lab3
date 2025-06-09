# Makefile for compiling serviceA, serviceB, and edge_client
# using gcc with the -lgpiod flag for GPIO access
CC = gcc
CFLAGS = -Wall -I.
LDFLAGS = -ljson-c -lgpiod
SRC = serviceA.c serviceB.c edge_client.c iot_ide.c
EXEC = serviceA serviceB edge_client iot_ide
all: $(EXEC)

serviceA: serviceA.c
	$(CC) $(CFLAGS) -o serviceA serviceA.c $(LDFLAGS)

serviceB: serviceB.c
	$(CC) $(CFLAGS) -o serviceB serviceB.c $(LDFLAGS)

edge_client: edge_client.c
	$(CC) $(CFLAGS) -o edge_client edge_client.c $(LDFLAGS)

iot_ide: iot_ide.c
	$(CC) $(CFLAGS) -o iot_ide iot_ide.c $(LDFLAGS)

clean:
	rm -f $(EXEC)