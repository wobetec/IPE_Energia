-- adciona algumas concessionarias, nesse caso ficticias
INSERT INTO concessionarias (name) VALUES (
    "Light S/A"
);

INSERT INTO concessionarias_tarifas (grupo_tarifario, modalidade, subgrupo, concessionaria_id, demanda_ponta, demanda_fora_ponta, ultrapassagem_demanda_ponta, ultrapassagem_demanda_fora_ponta, demanda_verde, ultrapassagem_demanda_verde, consumo_ponta, consumo_fora_ponta, consumo_b) VALUES(
    "A",
    "Azul",
    3,
    1,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9
);

INSERT INTO concessionarias (name) VALUES (
    "Enel"
);

INSERT INTO concessionarias_tarifas (grupo_tarifario, modalidade, subgrupo, concessionaria_id, demanda_ponta, demanda_fora_ponta, ultrapassagem_demanda_ponta, ultrapassagem_demanda_fora_ponta, demanda_verde, ultrapassagem_demanda_verde, consumo_ponta, consumo_fora_ponta, consumo_b) VALUES(
    "A",
    "Verde",
    1,
    2,
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90
);




INSERT INTO quarteis (name, sigla, concessionaria_id) VALUES("Luxium", "LUX", 1);

-- inicia o povoamento do grafo
ALTER TABLE hierarquia ADD LUX INTEGER NOT NULL DEFAULT 0;

-- adciona o primeiro item ao grafo
INSERT INTO hierarquia (quartel_id) VALUES (1);
