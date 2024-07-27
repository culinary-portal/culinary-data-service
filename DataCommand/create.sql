
    create table customers (
        account_enable boolean,
        account_expired boolean,
        account_locked boolean,
        credentials_expired boolean,
        customer_id bigserial not null,
        email varchar(255) not null unique,
        password varchar(255) not null,
        primary key (customer_id)
    );

    create table roles (
        customer_id bigint not null,
        role_id bigserial not null,
        role varchar(255) check (role in ('ADMIN','ANONYMOUS','USER')),
        primary key (role_id)
    );

    alter table if exists roles 
       add constraint role_customer_fk 
       foreign key (customer_id) 
       references customers;

    create table customers (
        account_enable boolean,
        account_expired boolean,
        account_locked boolean,
        credentials_expired boolean,
        customer_id bigserial not null,
        email varchar(255) not null unique,
        password varchar(255) not null,
        primary key (customer_id)
    );

    create table roles (
        customer_id bigint not null,
        role_id bigserial not null,
        role varchar(255) check (role in ('ADMIN','ANONYMOUS','USER')),
        primary key (role_id)
    );

    alter table if exists roles 
       add constraint role_customer_fk 
       foreign key (customer_id) 
       references customers;

    create table customers (
        account_enable boolean,
        account_expired boolean,
        account_locked boolean,
        credentials_expired boolean,
        customer_id bigserial not null,
        email varchar(255) not null unique,
        password varchar(255) not null,
        primary key (customer_id)
    );

    create table roles (
        customer_id bigint not null,
        role_id bigserial not null,
        role varchar(255) check (role in ('ADMIN','ANONYMOUS','USER')),
        primary key (role_id)
    );

    alter table if exists roles 
       add constraint role_customer_fk 
       foreign key (customer_id) 
       references customers;

    create table customers (
        account_enable boolean,
        account_expired boolean,
        account_locked boolean,
        credentials_expired boolean,
        customer_id bigserial not null,
        email varchar(255) not null unique,
        password varchar(255) not null,
        primary key (customer_id)
    );

    create table roles (
        customer_id bigint not null,
        role_id bigserial not null,
        role varchar(255) check (role in ('ADMIN','ANONYMOUS','USER')),
        primary key (role_id)
    );

    alter table if exists roles 
       add constraint role_customer_fk 
       foreign key (customer_id) 
       references customers;

    create table customers (
        account_enable boolean,
        account_expired boolean,
        account_locked boolean,
        credentials_expired boolean,
        customer_id bigserial not null,
        email varchar(255) not null unique,
        password varchar(255) not null,
        primary key (customer_id)
    );

    create table roles (
        customer_id bigint not null,
        role_id bigserial not null,
        role varchar(255) check (role in ('ADMIN','ANONYMOUS','USER')),
        primary key (role_id)
    );

    alter table if exists roles 
       add constraint role_customer_fk 
       foreign key (customer_id) 
       references customers;

    create table customers (
        account_enable boolean,
        account_expired boolean,
        account_locked boolean,
        credentials_expired boolean,
        customer_id bigserial not null,
        email varchar(255) not null unique,
        password varchar(255) not null,
        primary key (customer_id)
    );

    create table roles (
        customer_id bigint not null,
        role_id bigserial not null,
        role varchar(255) check (role in ('ADMIN','ANONYMOUS','USER')),
        primary key (role_id)
    );

    alter table if exists roles 
       add constraint role_customer_fk 
       foreign key (customer_id) 
       references customers;

    create table customers (
        account_enable boolean,
        account_expired boolean,
        account_locked boolean,
        credentials_expired boolean,
        customer_id bigserial not null,
        email varchar(255) not null unique,
        password varchar(255) not null,
        primary key (customer_id)
    );

    create table roles (
        customer_id bigint not null,
        role_id bigserial not null,
        role varchar(255) check (role in ('ADMIN','ANONYMOUS','USER')),
        primary key (role_id)
    );

    alter table if exists roles 
       add constraint role_customer_fk 
       foreign key (customer_id) 
       references customers;
