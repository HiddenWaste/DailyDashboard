
s.boot;

    SynthDef.new(\chord, {
        arg freq = 440, amp = 0.5, dur = 0.5;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.1), doneAction: 2);
        sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;
    
    Pbind(
        \instrument, \chord,
        \dur, 0.5,
        \amp, 0.5,
        \degree, Pseq([ A#min, D#maj, G#maj ], inf),
        \scale, Scale.<built-in method capitalize of str object at 0x0000018BAB799F50>(), 
        \root, 8,
        \octave, 4
    ).play;
    