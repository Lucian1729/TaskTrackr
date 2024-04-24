drop database if exists task_management_0;
create database task_management_0;
use task_management_0

-- Create the "users" table
CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE
);

-- Create indexes on username and email in the users table
CREATE UNIQUE INDEX idx_username ON users (username);
CREATE UNIQUE INDEX idx_email ON users (email);

-- Create the "tasks" table
CREATE TABLE tasks (
  task_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  due_date DATE,
  priority VARCHAR(255),
  status VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create index on user_id in tasks table
CREATE INDEX idx_user_id ON tasks(user_id);