/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [id]
      ,[description]
      ,[drugCode]
      ,[diseaseCode]
      ,[type]
  FROM [InteractionsDB].[dbo].[Interactions]