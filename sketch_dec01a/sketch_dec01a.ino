

// 


// Motor outputs:
// Left Motor:
// DI1 = Pin10
// DI2 = Pin 11
// Right Motor:
// DI1 = Pin6
// DI2 = Pin9
enum motor_dir{FWD = 0, REV = 1};
enum motor_id {LEFT = 0, RIGHT = 1};
enum motor_pins{LD1 = 10, LD2 = 11, RD1 = 6, RD2 = 5};
enum logic {TRUE = 1, FALSE = 0};
enum fsm_state {LINE, ARC };
enum motor_pwr {MOTOR_ON = 255, MOTOR_OFF = 0};
// fsm design:
// 
struct sub_xc {
	int islight;
	int state;
	int min_line;
	int max_line;
	int min_arc;
	int max_arc;

	int light_threshold;
	
	int line_to_arc;
	int arc_to_line;

};

struct chromosome {
	sub_xc light;
	sub_xc dark;
};

chromosome xc;

const int PHOTO_PIN = 0;
const int BUMPER_PIN = 2;

const int LIGHT_MIN = 300;
const int LIGHT_MAX = 330;
void init_motors() 
{
	pinMode(LD1, OUTPUT);
	pinMode(LD2, OUTPUT);
	pinMode(RD1, OUTPUT);
	pinMode(RD2, OUTPUT);
}

void set_motor(int id, int dir, char power)
{
	int d1, d2;
	d1 = 0;
        d2 = 0;
	switch(id) {
	case LEFT:
		d1 = LD1;
		d2 = LD2;
		break;
	case RIGHT:
		d1 = RD1;
		d2 = RD2;
                break;
	default:
		break;
	}

	if(dir == FWD) {
		analogWrite(d1, power);
		analogWrite(d2, 0);
	} else if (dir == REV) {
		analogWrite(d1, 0);
		analogWrite(d2, power);
	}

}


void setup() 
{
   
     init_motors();
     Serial.begin(9600);
     randomSeed(analogRead(0));

     
     pinMode(13, OUTPUT);
     digitalWrite(13,1);
     delay(2000);
     digitalWrite(13,0);
     digitalWrite(7,0);
     pinMode(7, OUTPUT);
     pinMode(BUMPER_PIN, INPUT);           // set pin to input
     digitalWrite(BUMPER_PIN, HIGH);       // turn on pullup resistors

     xc.light = {
	     .islight = TRUE,
	     .state = LINE,
	     .min_line = 80,
	     .max_line = 100,
	     .min_arc = 100,
	     .max_arc = 150,
	     
	     .light_threshold = 300,

	     .line_to_arc = 500
,

	     .arc_to_line = 500,
     };

     xc.dark = {
	     .islight = FALSE,
             .state = LINE,
	     .min_line = 50,
	     .max_line = 100,
	     .min_arc = 50,
	     .max_arc = 60,
	     
	     .light_threshold = 310,

	     .line_to_arc = 700,
	     .arc_to_line = 400,
     };


}

void smart_delay(int len)
{
	for(int i = 0; i < len - 1; i++) {
		delay(10); //10ms delay quantum
		if(digitalRead(BUMPER_PIN) == 1) {
			set_motor(LEFT, REV, MOTOR_ON);
			set_motor(RIGHT, REV, MOTOR_ON);
			Serial.println("Hit a wall");
			delay(1000);
			return;
		}
	}

}



void update_xc(struct sub_xc * curxc)
{
	// checkif if we should switch from line to arc
	if(state == LINE) {
		if(random(1000) < curxc->line_to_arc) {
			state = ARC;
		} 
	} else {
		if(random(1000) < curxc->arc_to_line) {
			state = LINE;
		} 
	}
}
void fuzzy_mixer(struct chromosome * c_xc, int lightval)
{
	int p_range = LIGHT_MAX - LIGHT_MIN;
	int dark_value = lightval - LIGHT_MIN;
	int light_value = p_range - lightval - LIGHT_MIN;
	int rval;


	int rd_power = c_xc->dark.state == LINE ? 255 : -255;
	int rl_power = c_xc->light.state == LINE ? 255 : -255;

	int r_power = (rd_power * dark_value + rl_power * light_value) / p_range;
	int l_power = 255;

	int d_time, l_time;
	if(c_xc->dark.state == LINE) {
		d_time = random(c_xc->dark.max_line - c_xc->dark.min_line) + 
		c_xc->dark.min_line;
	} else {
		d_time = random(c_xc->dark.max_arc - c_xc->dark.min_arc) + 
		c_xc->dark.min_arc;		
	}

	if(c_xc->light.state == LINE) {
		l_time = random(c_xc->light.max_line - c_xc->light.min_line) + 
		c_xc->light.min_line;
	} else {
		l_time = random(c_xc->light.max_arc - c_xc->light.min_arc) + 
		c_xc->light.min_arc;		
	}

	int r_time = (d_time * dark_value + l_time * light_value) / p_range;

	int r_dir = r_power < 0 ? REV : FWD;
	r_power = r_power < 0 ? r_power * -1 : r_power;
	
	set_motor(LEFT, FWD, MOTOR_ON);
	set_motor(RIGHT, r_dir, r_power);

	smart_delay(r_time);
	
	set_motor(LEFT, FWD, MOTOR_OFF);
	set_motor(RIGHT, FWD, MOTOR_OFF);


	
}

void loop () 
{
	

	int photo = analogRead(PHOTO_PIN);
	fuzzy_mixer(&xc, photo);

	update_xc(&xc.light);
	update_xc(&xc.dark);
}



