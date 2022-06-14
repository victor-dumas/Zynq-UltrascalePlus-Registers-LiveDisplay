# Zynq-UltrascalePlus-Registers-LiveDisplay

This flask server can be used to get the status of the the ultrascale+ soc registers.
It is based on the listing of registers found at https://www.xilinx.com/htmldocs/registers/ug1087/ug1087-zynq-ultrascale-registers.html.

A tcp server(devmem_server) is used on the target to get the register values. This server requires that the linux allows full devmem access.

  
TODO:
- Improve performance of the live display
