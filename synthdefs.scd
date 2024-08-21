SynthDef.new(\\chord, {
        arg freq = 440, amp = 0.5, dur = 0.5;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.1), doneAction: 2);
        sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;

SynthDef.new(\\bass, {
        arg freq = 220, amp = 0.3, dur = 1.0;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.2), doneAction: 2);
        sig = Saw.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;

SynthDef.new(\\lead, {
        arg freq = 880, amp = 0.7, dur = 0.3;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.3), doneAction: 2);
        sig = Saw.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;

SynthDef.new(\\glockenspiel, {
        arg freq = 1046.5, amp = 0.4, dur = 0.2;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.2), doneAction: 2);
        sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;

SynthDef.new(\\harp, {
        arg freq = 440, amp = 0.5, dur = 0.5;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.1), doneAction: 2);
        sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;

SynthDef.new(\\kalimba, {
        arg freq = 440, amp = 0.5, dur = 0.5;
        var env, sig;
        env = EnvGen.kr(Env.perc(0.01, 0.1), doneAction: 2);
        sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, sig);
    }).add;