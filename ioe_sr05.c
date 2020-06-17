void main (void) {
    com_initialize (); /* initialize interrupt driven serial I/O */ 
    com_baudrate (9600); /* setup for 9600 baud */ 
    EA = 1; // Enable Interrupts 
    while (1) {
        Unsigned char head,dh,dl,sum;
        Head = com_getchar();
        If (head != 0xff) 
            continue;
        Dh = com_getchar();
        Dl = com_getchar();
        Sum = com_getchar();
        Head = head + dh + dl;
        If (head != sum)
            continue; //and checksum error
        // now dh * 256 + dl is the measured distance value,
        // and then further processing... 
    } 
}