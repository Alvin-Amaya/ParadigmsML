:- module(engine,
[
    diagnose/2
]).

:- use_module(knowledge).
:- use_module(patient).
:- use_module(library(lists)).

evaluate(Patient,
         Finding,
         true,
         [Finding]) :-

    patient:fact(Patient,Finding).

evaluate(_,
         Finding,
         false,
         [missing(Finding)]).

evaluate(Patient,
         all([]),
         true,
         []).

evaluate(Patient,
         all([H|T]),
         Result,
         Evidence):-
    evaluate(Patient,H,R1,E1),
    evaluate(Patient,all(T),R2,E2),
    append(E1,E2,Evidence),

    (
        R1==true,
        R2==true
    ->
        Result=true
    ;
        Result=false
    ).

evaluate(Patient,
         any(List),
         Result,
         Evidence):-

    evaluate_any(Patient,
                 List,
                 Result,
                 Evidence).

evaluate_any(_,[],
             false,
             []).

evaluate_any(Patient,
             [H|_],
             true,
             Evidence):-

    evaluate(Patient,
             H,
             true,
             Evidence),
    !.

evaluate_any(Patient,
             [_|T],
             Result,
             Evidence):-

    evaluate_any(Patient,
                 T,
                 Result,
                 Evidence).

evaluate(Patient,
         not(X),
         true,
         []) :-

    evaluate(Patient,
             X,
             false,
             _).

evaluate(Patient,
         not(_),
         false,
         []).

evaluate_rule(Patient,
              RuleID,
              Score,
              Explanation):-

    knowledge:rule(
        RuleID,
        Disease,
        Condition,
        Weight),

    evaluate(Patient,
             Condition,
             Result,
             Evidence),

    (
        Result==true

    ->

        Score=Weight

    ;

        Score=0
    ),

    Explanation=
        explanation(
            Disease,
            RuleID,
            Result,
            Evidence,
            Score
        ).

score_disease(
    Patient,
    Disease,
    Total,
    Explanations):-

    findall(

        Rule,

        knowledge:rule(
            Rule,
            Disease,
            _,
            _),

        Rules),

    evaluate_rules(
        Patient,
        Rules,
        Total,
        Explanations).

evaluate_rules(
    _,
    [],
    0,
    []).

evaluate_rules(
    Patient,
    [R|Rs],
    Total,
    [Exp|Exps]):-

    evaluate_rule(
        Patient,
        R,
        Score,
        Exp),

    evaluate_rules(
        Patient,
        Rs,
        Partial,
        Exps),

    Total is
        Score+Partial.

diagnose(
    Patient,
    Results):-

    findall(

        Disease,

        knowledge:entity(
            Disease,
            disease),

        Diseases),

    diagnose_all(
        Patient,
        Diseases,
        Results).

diagnose_all(
    _,
    [],
    []).

diagnose_all(
    Patient,
    [Disease|Rest],
    [diagnosis(
        Disease,
        Score,
        Explanation)|Tail]):-

    score_disease(
        Patient,
        Disease,
        Score,
        Explanation),

    diagnose_all(
        Patient,
        Rest,
        Tail).