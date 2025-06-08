// iot_ide.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define EDGE_IP "127.0.0.1"
#define EDGE_CMD_PORT 7000



int main() {
    char command[256];
    char response[256];

    while (1) {
        printf("iot> ");
        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = '\0'; // remove newline

        if (strcmp(command, "exit") == 0)
            break;

        int sock = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in edge_addr;
        edge_addr.sin_family = AF_INET;
        edge_addr.sin_port = htons(EDGE_CMD_PORT);
        inet_pton(AF_INET, EDGE_IP, &edge_addr.sin_addr);

        if (connect(sock, (struct sockaddr *)&edge_addr, sizeof(edge_addr)) < 0) {
            perror("Error connecting to edge_client");
            continue;
        }

        send(sock, command, strlen(command), 0);
        memset(response, 0, sizeof(response));
        recv(sock, response, sizeof(response), 0);
        printf("Edge response: %s\n", response);

        close(sock);
    }

    return 0;
}
