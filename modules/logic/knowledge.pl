:- module(knowledge,
[
    entity/2,
    rule/4
]).

entity(covid,disease).
entity(gripe,disease).
entity(neumonia,disease).

entity(fiebre,symptom).
entity(tos,symptom).
entity(anosmia,symptom).
entity(disnea,symptom).

rule(r1,covid,
    all([fiebre,tos]),
    40).

rule(r2,covid,
    anosmia,
    60).

rule(r3,gripe,
    all([fiebre,tos]),
    50).

rule(r4,neumonia,
    all([fiebre,disnea]),
    80).