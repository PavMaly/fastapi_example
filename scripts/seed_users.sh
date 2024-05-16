#!/bin/bash

#salt = 08299abd2a9b6090ccac621a4bb64f8c326820240b26abfeed359822cf5e78b3
psql --set ON_ERROR_STOP=OFF -h localhost -U "app" -d "app"<<-EOSQL
-- пользователи
  CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  is_admin BOOL DEFAULT false,
  is_librarian BOOL DEFAULT false,
  password VARCHAR(150) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  DELETE FROM users;
  ALTER SEQUENCE users_user_id_seq RESTART WITH 1;

  INSERT INTO users (username, is_admin, is_librarian, password) values
    ('admin', true, false, '8b5087c004ede3c8cf3ae056f8b0c14c30f095957922c9ed692d59885b46889710d4002f768f6673b9a1784b47d0ba2615f43048ee5d7ea0efbd15927e4bf3e6'),               -- qwerty123456
    ('barsik', true, true, 'f94557c2882896b08a83c8d35ab6523e8733dd9cfd1ff4a9cea709bec96596b8055ade12c77763a46a6b2a04d5afdc84a8a4be4de373bf8031a8fd45fa8d31d1'),               -- books4ever
    ('serrios_one', false, true, 'a43aedb70d56992545993b10bf5134e80813c38eb80c10225b9a0d9eb136a415d121732c7f3baa7d1382ebd8103dcd7d710c32a1126e1d1984945b98df9b243f'),         -- StrongPass!22
    ('evil_genius', false, false, '8c4404b2fedc18b8de6af34868d34f0e6a2033af869412b0fa1b3a66a1a63b91bdc62343f65a542aa7b73671bd1f4ad4db7f837a04916c2448930e5a165bf09b'),        -- Dance!Dance!Dance!
    ('igor_gromov', false, false, '95c0ed4abe458c8d54ca6eb629ff1a618755dcbea2b2e9a41858cc616db3c51d34f9b415713ae977c6827d15a4d17e330283229a01350b2d6b877f6eafe03376');        -- DuraLexSedLex

  CREATE TABLE IF NOT EXISTS users_data(
    user_id INTEGER UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(50) DEFAULT '--',
    address VARCHAR(150) DEFAULT '--',
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE);

  DELETE from users_data;

  INSERT INTO users_data (user_id, full_name, email, phone, address) values
    (1, 'Иванов Иван', 'admin@library.org', null, null),
    (2, 'Петров Петр', 'cat@library.org', null, null),
    (3, 'Пылаева Мария', 'pylaeva.mv@library.org', null, null),
    (4, 'Разумовский Сергей', 'thedoctor@vmeste.ru', '+79004447777', '197110 Санкт-Петербург, ул. Большая Зеленина, 11/1 литера А, 18'),
    (5, 'Громов Игорь', 'igor_gromov@glavk.ru', '89003335555', '190000 Санкт-Петербург, пр-кт Невский, 70 литера А, 22');
EOSQL