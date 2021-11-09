# radar_detection_OGSC
Title completes me\\
CSGO hacks 
## How to start

### What do I need 
--Python
--Pymem
####
What is Pymem and how should I download it?

https://pip.pypa.io/en/stable/installation/

```python
py get-pip.py
pip3 install pymem
```
### Radar 
Start CS:GO by double-clicking activation.py or entering the python activation.py command. Despite the fact that the application is immediately available, the hack only works as long as the game is active. Simply restart activation.py to restart hack without restarting.

### Wallhack
This program patches assembly code produced by compiling the [following line of the game code](https://github.com/ValveSoftware/source-sdk-2013/blob/0d8dceea4310fde5706b3ce1c70609d72a38efdf/mp/src/game/client/c_baseanimating.cpp#L3149):
```cpp
int extraFlags = 0;
if ( r_drawothermodels.GetInt() == 2 )
{	
    extraFlags |= STUDIO_WIREFRAME;	
}
```
### Show enemy's money
Display enemies' money, patching one byte of game memory

### B_hop
```python
pip3 install Pymem
pip3 install keyboard
pip3 install pywin32api
python bunny.py
```


### What's next
