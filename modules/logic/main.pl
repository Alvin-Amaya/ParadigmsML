:- use_module(engine).
:- use_module(patient).

run:-

    clear_patient(patient),

    add_fact(patient,fiebre),

    add_fact(patient,tos),

    add_fact(patient,anosmia),

    diagnose(patient,R),

    writeln(R).