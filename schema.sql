create table pokemon (
  survey_id SERIAL PRIMARY KEY,
  name1 varchar(255) NOT NULL,
  type1 text,
  region text,
  ta text,
  ColumnDateTime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO pokemon (name1, type1, region, ta) VALUES('Charmander','Fire','Kanto', 'I Love Fire Types');