:- module(patient,
[
    fact/2,
    add_fact/2,
    clear_patient/1
]).

:- dynamic fact/2.

add_fact(Patient,Fact):-

    assertz(fact(Patient,Fact)).

clear_patient(Patient):-

    retractall(fact(Patient,_)).