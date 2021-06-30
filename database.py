import pymssql


def CreateDataBase():
     with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976', database='ELAL') as conn:
        query ='CREATE DATABASE "ELAL"'
        conn.execute_query(query)

     with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976', database='ELAL') as conn:
         query = 'CREATE TABLE [dbo].[users]([id_AI][int] IDENTITY(1, 1) NOT NULL,[full_name][varchar](50) NOT NULL,[password][varchar](50) NOT NULL,[real_id][varchar](50) NOT NULLCONSTRAINT [PK_users] PRIMARY KEY CLUSTERED ([id_AI] ASC)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]) ON [PRIMARY]'
         conn.execute_query(query)
     with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976', database='ELAL') as conn:
        query = 'CREATE TABLE [dbo].[Tickets]([ticket_id][int] IDENTITY(1,1) NOT NULL,[user_id] [int] NOT NULL,[flight_id] [int] NOT NULL,CONSTRAINT [PK_Tickets] PRIMARY KEY CLUSTERED([ticket_id] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]) ON [PRIMARY]'
        conn.execute_query(query)
     with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976', database='ELAL') as conn:
         query='CREATE TABLE [dbo].[Flights]([flights_id] [int] IDENTITY(1,1) NOT NULL,[timestamp] [datetime] NOT NULL,[remaining_seats] [int] NULL,[orgin_country_id] [int] NOT NULL,[dest_country_id] [int] NOT NULL,CONSTRAINT [PK_Flights] PRIMARY KEY CLUSTERED([flights_id] ASC)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]) ON [PRIMARY]'
         conn.execute_query(query)
     with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976', database='ELAL') as conn:
          query='CREATE TABLE [dbo].[countries]([code_AL] [int] IDENTITY(1,1) NOT NULL,[name] [varchar](50) NOT NULL,CONSTRAINT [PK_countries] PRIMARY KEY CLUSTERED ([code_AL] ASC)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]) ON [PRIMARY]'