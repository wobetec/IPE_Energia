-- adciona a OM principal, nesse caso uma ficticia
INSERT INTO quarteis (name, sigla, efetivo, area, grupo_tarifario, demanda_contratada) VALUES("EB Energia", "EBE", 0, 0, "", 0);

-- inicia o povoamento do grafo
ALTER TABLE hierarquia ADD EBE INTEGER NOT NULL DEFAULT 0;

-- adciona o primeiro item ao grafo
INSERT INTO hierarquia (quartel_id) VALUES (1);
