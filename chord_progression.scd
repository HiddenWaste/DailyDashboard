
s.boot;

SynthDef.new(\glockenspiel, {
        arg freq = 1046.5, amp = 0.4, dur = 0.2;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.2), doneAction: 2);
        sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;

    Pbind(
        \instrument, \glockenspiel,           // Use the chosen synth
        \dur, 0.5,                                  // Duration of each note
        \amp, 0.5,                                  // Amplitude of each note
        \degree, Pseq([ 2, 5 ], inf),     // A Pseq that cycles through the progression's notes (degrees) the inf means it will loop forever
        \scale, Scale.major,               // The scale to use
        \root, 0,
        \octave, 4
    ).play;
 s.quit;
