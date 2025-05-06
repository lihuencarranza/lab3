# Makefile for compiling and executing GPIO test programs

CC = gcc
CFLAGS = -o
SRC = serviceA.c serviceB.c edge_client
EXEC = serviceA serviceB edge_client
all: $(EXEC)

serviceA: serviceA.c
	$(CC) $(CFLAGS) serviceA serviceA.c -lgpiod

serviceB: serviceB.c
	$(CC) $(CFLAGS) serviceB serviceB.c -lgpiod

edge_client: edge_client.c
	$(CC) $(CFLAGS) edge_client edge_client.c -lgpiod

clean:
	rm -f $(EXEC)