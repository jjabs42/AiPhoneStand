# A functional phone stand face tracker 

# Hardware Dependencies
Arduino R4 Wifi  
2 Mg996r [Servo motors][1]  
4 AA Battery Holder  


## Quick Start
---
Install Dependencies 
```bash
pip install -r requirements.txt
```
---
HOW TO BUILD INCLUDED IN THE FUTURE
1. Go to hardware/platformio/src/code.cpp on line 187 and replace with your computers current IP

---
### Running
1. Open the Platformio Session found in Hardware
2. Push code to Arduino R4
3. Run 
```bash
 python -m software.src.frontend.flask_frontend_server.app
```
- NOTE: The arduino needs to be turned on so it can connect to the websocket
4. Visit the IP of your computer on port 5555  (IP:5555) on a web browser with the desired phone
5. Calibrate 
6. Start tracking

MORE FEATURES LIKE VIDEOS WILL BE ADDED










[1]: https://www.amazon.com/4-Pack-MG996R-Torque-Digital-Helicopter/dp/B07MFK266B/ref=sr_1_4_sspa?crid=3UKHNQTVLXHDE&dib=eyJ2IjoiMSJ9.cwyQrvZadS8g8__InaWqbFAutkCElGdoiAG-mrB75Lxw0UMsByyxwmZnhm_rzOjJ3bL73WADGhE5mYhh9LJpVnZiOG17nGd8-AcJeHTXCKyDjfvx7pA_KIJZG9SjSVAdCDOTEkmMa3Zlo8s_fRWUXnVG4bZnWr4tJP2jrZRk5JGEtnqLyty0ghkAG7SP92WRTh9CQrw6gdzjmQEedH7HhEs0HRMSjj4-ocrOqzPMMFVyW9urc8IIJiMKI5aNteSe7A8epkwhG6floJMtKp1dLPkVX79ZLlQaoIQTG2A9DPU.At-CGTYNywLPBkujejv4nsbCg4dRXVc90bc5zbU-hVQ&dib_tag=se&keywords=servo%2Bmotor&qid=1783898176&sprefix=servo%2Bmotor%2Caps%2C140&sr=8-4-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1

