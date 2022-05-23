#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/time.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <netinet/in.h>
#include <signal.h>
#include <netdb.h> 
#include <string.h> 

#include <regex.h>

#define MAX 2+10+8+2
#define MAX_LEN 512
#define SA struct sockaddr 
#define VERSION "28/02/22, 16H26"

void print_help()
{
    printf("W: write R: read A: address D: data\n");
    printf("Command can be of type WAAAAAAAAADDDDDDD with an answer WAAAAAAAAA\n");
    printf("Command can be of type WNAAAAAAAAAADDDDDDD with an answer WNAAAAAAAAA\n");
    printf("Command can be of type RAAAAAAAAA with an answer RAAAAAAAAADDDDDDDD\n");
    printf("Command can be of type RNAAAAAAAAA with an answer RNAAAAAAAAADDDDDDDD\n");
}

void usage(char *prog)
{
	printf("usage: %s PORT\n",prog);
	printf("exemple: %s  4001\n",prog);
	printf("\n");
	printf("Once started commands are:\n");
	print_help();
}

unsigned read_register(u_int64_t addr)
{
	u_int32_t value=0;

	// Call of devmem 
	char cmd[MAX_LEN];
	sprintf(cmd, "/sbin/devmem 0x%08x", addr);
	FILE * f = popen(cmd, "r");
    char ret_cmd[MAX_LEN] = {0};
    fgets(ret_cmd, MAX_LEN, f);
    pclose(f);

    regex_t    preg;
	regmatch_t pmatch[2];
   
    // Regex compilation
    regcomp(&preg, "0x([0-9a-fA-F]{8,8})", REG_EXTENDED );
    
    int ret=regexec(&preg, ret_cmd, 2, pmatch, 0);
    regfree(&preg);
    if (ret != REG_NOMATCH)
    {
    	// Get addr to an hex string
    	char data_str[8+1];
    	strncpy(data_str, ret_cmd + pmatch[1].rm_so, 8);
    	data_str[8] =0;

    	u_int64_t data;
        // Convert hex string to int
    	value=strtoll(data_str, NULL, 16);
    }

	return value;
}

unsigned write_register(u_int64_t addr, u_int32_t val)
{
	// Call devmem
	char cmd[MAX_LEN];
	sprintf(cmd, "/sbin/devmem 0x%08x 32 0x%08x", addr, val);
	
    FILE * f = popen(cmd, "r");
    char ret_cmd[MAX_LEN] = {0};
    fgets(ret_cmd, MAX_LEN, f);
    pclose(f);

	return 0;
}

// Returns 1 if pattern is detected with addr_detected and data_datected. 0 otherwise
int search_write_pattern(char *line, u_int64_t *addr_detected, u_int32_t *data_datected)
{
    regex_t    preg;
	regmatch_t pmatch[3];
   
    regcomp(&preg, "W([0-9a-fA-F]{9,9})([0-9a-fA-F]{8,8})", REG_EXTENDED );
    
    int ret=regexec(&preg, line, 3, pmatch, 0);
    regfree(&preg);
    if (ret != REG_NOMATCH)
    {
    	char addr_str[9+1];
    	strncpy(addr_str, line + pmatch[1].rm_so, 9);
    	addr_str[9] =0;

    	u_int64_t addr;
    	addr=strtoll(addr_str, NULL, 16);

    	char data_str[8+1];
    	strncpy(data_str, line + pmatch[2].rm_so, 8);
    	data_str[8] =0;

    	u_int32_t data;
    	data=strtol(data_str, NULL, 16);

    	*addr_detected= addr;
    	*data_datected= data;
    	return 1;
    }
    else
    	return 0;
}

int search_write_pattern_new(char *line, u_int64_t *addr_detected, u_int32_t *data_datected)
{
    regex_t    preg;
	regmatch_t pmatch[3];
   
    regcomp(&preg, "WN([0-9a-fA-F]{10,10})([0-9a-fA-F]{8,8})", REG_EXTENDED );
    
    int ret=regexec(&preg, line, 3, pmatch, 0);
    regfree(&preg);
    if (ret != REG_NOMATCH)
    {
    	char addr_str[10+1];
    	strncpy(addr_str, line + pmatch[1].rm_so, 10);
    	addr_str[10] =0;

    	u_int64_t addr;
    	addr=strtoll(addr_str, NULL, 16);

    	char data_str[8+1];
    	strncpy(data_str, line + pmatch[2].rm_so, 8);
    	data_str[8] =0;

    	u_int32_t data;
    	data=strtol(data_str, NULL, 16);

    	*addr_detected= addr;
    	*data_datected= data;
    	return 1;
    }
    else
    	return 0;
}

int search_read_pattern(char *line, u_int64_t *addr_detected)
{
    regex_t    preg;
	regmatch_t pmatch[2];
   
    regcomp(&preg, "R([0-9a-fA-F]{9,9})", REG_EXTENDED );
    
    int ret=regexec(&preg, line, 2, pmatch, 0);
    regfree(&preg);
    if (ret != REG_NOMATCH)
    {
    	char addr_str[9+1];
    	strncpy(addr_str, line + pmatch[1].rm_so, 9);
    	addr_str[9] =0;

    	u_int64_t addr;
    	addr=strtoll(addr_str, NULL, 16);

    	*addr_detected= addr;
    	return 1;
    }
    else
    	return 0;
}

int search_read_pattern_new(char *line, u_int64_t *addr_detected)
{
    regex_t    preg;
	regmatch_t pmatch[2];
   
    regcomp(&preg, "RN([0-9a-fA-F]{10,10})", REG_EXTENDED );
    
    int ret=regexec(&preg, line, 2, pmatch, 0);
    regfree(&preg);
    if (ret != REG_NOMATCH)
    {
    	char addr_str[10+1];
    	strncpy(addr_str, line + pmatch[1].rm_so, 10);
    	addr_str[10] =0;

    	u_int64_t addr;
    	addr=strtoll(addr_str, NULL, 16);

    	*addr_detected= addr;
    	return 1;
    }
    else
    	return 0;
}


int main(int argc, char *argv[])
{
    int sockfd, connfd, len; 
    struct sockaddr_in servaddr, cli; 
    char buff[MAX]; 
    int port;

	if(argc == 2 ) {
		port=strtol(argv[1], NULL, 0); 
	}
	else if (argc == 1)
	{
		port=4001; 
	}
	else
	{
		usage(argv[0]);
		exit(-1);
	}
	
	printf("port=%d\n", port);

    sockfd = socket(PF_INET, SOCK_STREAM, 0); 
    if (sockfd == -1) { 
        printf("socket creation failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully created..\n"); 
    int optval = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(int));
    bzero(&servaddr, sizeof(servaddr)); 

  	// assign IP, PORT 
    servaddr.sin_family = AF_INET; 
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
    servaddr.sin_port = htons(port); 
  
    // Binding newly created socket to given IP and verification 
    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) { 
        printf("socket bind failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully binded..\n"); 
  
    printf("Version :%s\n", VERSION);
    printf("Serveur started on port %d\n", port);

    print_help();

    // Now server is ready to listen and verification 
    if ((listen(sockfd, 5)) != 0) { 
        printf("Listen failed...\n"); 
        exit(0); 
    } 
    else
        printf("Server listening..\n"); 
    len = sizeof(cli); 
 	
    while(1)  { 

	    // Accept the data packet from client and verification 
	    connfd = accept(sockfd, (SA*)&cli, &len); 
	    if (connfd < 0) { 
	        printf("server accept failed...\n"); 
	        exit(0); 
	    } 
	    else
	        printf("server accept the client...\n"); 

		// infinite loop for command
	    int match;
		u_int32_t data;
		u_int64_t addr;
	    while(1) { 
	        bzero(buff, MAX); 
	  
	        // read the message from client and copy it in buffer 
	        int ret=recv(connfd, buff, sizeof(buff),0); 
	        if (ret == 0)
	        {
	            printf("Connexion stop...\n"); 
	            //close(sockfd); 
	            break; 
	        }
	        printf("Received %s",buff);
		    fflush(stdout);
	        if ( (match=search_write_pattern_new(buff, &addr, &data)) == 1) 
	        {
				write_register(addr, data);
				sprintf(buff, "WN%010lx\n\r", addr);
		        write(connfd, buff, 2+10+2); 

		    } else if ( (match=search_write_pattern(buff, &addr, &data)) == 1) 
		    {
				write_register(addr, data);
				sprintf(buff, "W%09lx\n\r", addr);
		        write(connfd, buff, 1+9+2); 
		    } else if ( (match=search_read_pattern_new(buff, &addr)) == 1)
		    {
		    	data= read_register(addr);
				sprintf(buff, "RN%010lx%08x\n\r", addr, data);
		        write(connfd, buff, 1+9+8+2); 
		    }else if ( (match=search_read_pattern(buff, &addr)) == 1)
		    {
		    	data= read_register(addr);
				sprintf(buff, "R%09lx%08x\n\r", addr, data);
		        write(connfd, buff, 1+9+8+2); 
		    }
	  
	        if (strncmp("exit", buff, 4) == 0) { 
	            printf("Server Exit...\n"); 
			    close(sockfd); 
				return 0;
	        }         	
	    }     
	}     
}

