CREATE TABLE IF NOT EXISTS concessionarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS concessionarias_tarifas (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    concessionaria_id INTEGER NOT NULL,

    grupo_tarifario TEXT DEFAULT NULL,
    modalidade TEXT DEFAULT NULL,
    subgrupo INTEGER DEFAULT NULL,
    demanda_ponta REAL DEFAULT NULL,
    demanda_fora_ponta REAL DEFAULT NULL,
    ultrapassagem_demanda_ponta REAL DEFAULT NULL,
    ultrapassagem_demanda_fora_ponta REAL DEFAULT NULL,
    demanda_verde REAL DEFAULT NULL,
    ultrapassagem_demanda_verde REAL DEFAULT NULL,
    consumo_ponta REAL DEFAULT NULL,
    consumo_fora_ponta REAL DEFAULT NULL,
    consumo_b REAL DEFAULT NULL,

    FOREIGN KEY (concessionaria_id) 
        REFERENCES concessionarias(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS quarteis (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    sigla TEXT NOT NULL UNIQUE,
    brasao TEXT DEFAULT "",
    efetivo INTEGER DEFAULT NULL,
    area REAL DEFAULT NULL,

    tem_subordinado INTEGER DEFAULT 0,
    tem_geracao_distribuida INTEGER DEFAULT 0,

    tolerancia_ultrapassagem_demanda REAL DEFAULT NULL,
    concessionaria_id INTEGER NOT NULL,
    grupo_tarifario TEXT DEFAULT NULL,
    modalidade TEXT DEFAULT NULL,
    subgrupo INTEGER DEFAULT NULL,

    FOREIGN KEY (concessionaria_id) 
        REFERENCES concessionarias(id)
);

CREATE TABLE IF NOT EXISTS quarteis_demanda_contratada (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quartel_id INTEGER NOT NULL,
    umida_ponta REAL DEFAULT NULL,
    umida_fora_ponta REAL DEFAULT NULL,
    seca_ponta REAL DEFAULT NULL,
    seca_fora_ponta REAL DEFAULT NULL,
    umida REAL DEFAULT NULL,
    seca REAL DEFAULT NULL,

    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE

);


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    quartel_id INTEGER NOT NULL,
    access_level INTEGER NOT NULL,

    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
);


CREATE TABLE IF NOT EXISTS despesas(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quartel_id INTEGER NOT NULL,
    efetivo INTEGER NOT NULL,
    area REAL NOT NULL,

    valor REAL NOT NULL,
    multa REAL DEFAULT NULL,
    data_fatura TEXT NOT NULL,

    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS despesas_demanda_contratada(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    despesa_id INTEGER NOT NULL,
    umida_ponta REAL DEFAULT NULL,
    umida_fora_ponta REAL DEFAULT NULL,
    seca_ponta REAL DEFAULT NULL,
    seca_fora_ponta REAL DEFAULT NULL,
    umida REAL DEFAULT NULL,
    seca REAL DEFAULT NULL,

    FOREIGN KEY (despesa_id) 
        REFERENCES despesas(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS despesas_tarifas(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    despesa_id INTEGER NOT NULL,

    demanda_ponta REAL DEFAULT NULL,
    demanda_fora_ponta REAL DEFAULT NULL,
    ultrapassagem_demanda_ponta REAL DEFAULT NULL,
    ultrapassagem_demanda_fora_ponta REAL DEFAULT NULL,
    demanda_verde REAL DEFAULT NULL,
    ultrapassagem_demanda_verde REAL DEFAULT NULL,
    consumo_ponta REAL DEFAULT NULL,
    consumo_fora_ponta REAL DEFAULT NULL,
    consumo_b REAL DEFAULT NULL,

    FOREIGN KEY (despesa_id) 
        REFERENCES despesas(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS despesas_consumo(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    despesa_id INTEGER NOT NULL,

    energia_ativa REAL DEFAULT NULL,
    energia_reativa REAL DEFAULT NULL,
    ponta REAL DEFAULT NULL,
    fora_ponta REAL DEFAULT NULL,
    demanda_consumida REAL DEFAULT NULL,
    demanda_consumida_ponta REAL DEFAULT NULL,
    demanda_consumida_fora_ponta REAL DEFAULT NULL,

    FOREIGN KEY (despesa_id) 
        REFERENCES despesas(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS geradores(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quartel_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    tipo TEXT NOT NULL,

    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS geracao(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    gerador_id INTEGER NOT NULL,
    efetiva REAL NOT NULL,
    reativa REAL NOT NULL,
    consumo REAL NOT NULL,
    data_uso TEXT NOT NULL,

    FOREIGN KEY (gerador_id) 
        REFERENCES geradores(id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS hierarquia(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quartel_id INTEGER NOT NULL,
    
    FOREIGN KEY (quartel_id) 
        REFERENCES quarteis(id)
);


