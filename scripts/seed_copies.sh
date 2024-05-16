#!/bin/bash

psql --set ON_ERROR_STOP=OFF -h localhost -U "app" -d "app"<<-EOSQL
-- Экземпляры
  -- Статусы
  CREATE TABLE IF NOT EXISTS copy_statuses (
  status_id SERIAL PRIMARY KEY,
  description VARCHAR(255)
  );

  DELETE FROM copy_statuses;
  ALTER SEQUENCE copy_statuses_status_id_seq RESTART WITH 1;

  INSERT INTO copy_statuses (description) values
  ('in_collection'), ('given_out'), ('retired');


  CREATE TABLE IF NOT EXISTS copies(
    copy_id int generated always as identity (start 100001) primary key,
    book_id int,
    status_id int,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES copy_statuses (status_id) ON DELETE CASCADE
   );

  DELETE FROM copies;
  ALTER SEQUENCE  copies_copy_id_seq  RESTART WITH 100001;

  INSERT INTO copies (book_id, status_id, created_at, updated_at) values
  (1, 1, NOW() - INTERVAL '30 day', NOW() - INTERVAL '30 day'),
  (2, 1, NOW() - INTERVAL '20.99 day', NOW() - INTERVAL '20.99 day'),
  (3, 1, NOW() - INTERVAL '20.98 day', NOW() - INTERVAL '20.98 day'),
  (4, 1, NOW() - INTERVAL '20.5 day', NOW() - INTERVAL '20.5 day'),
  (5, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (6, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (7, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (7, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (7, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (7, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (8, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (8, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (9, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (10, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (11, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (12, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (13, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (14, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (14, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (15, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (16, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (17, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (18, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (19, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (20, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (21, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (22, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (23, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (24, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day'),
  (25, 1, NOW() - INTERVAL '10 day', NOW() - INTERVAL '10 day');


EOSQL