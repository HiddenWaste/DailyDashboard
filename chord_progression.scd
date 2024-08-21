
s.boot;

SynthDef.new(\pulse, {
    arg freq = 440, amp = 0.5, dur = 0.5, width = 0.5;
    var env, sig;
    env = EnvGen.kr(Env.perc(0.01, 0.1), doneAction: 2);
    sig = Pulse.ar(freq, width) * amp * env;
    Out.ar([0, 1], sig);
    }).add;

    Pbind(
        \instrument, \pulse,           // Use the chosen synth
        \dur, 0.5,                                  // Duration of each note
        \amp, 0.2,                                  // Amplitude of each note
        \degree, Pseq([ 1, 4, 5, 1 ], inf),     // A Pseq that cycles through the progression's notes (degrees) the inf means it will loop forever
        \scale, Scale.major,               // The scale to use
        \root, 0,                             
        \octave, 4
    ).play;
    
