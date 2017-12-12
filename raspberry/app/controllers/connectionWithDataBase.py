#!/usr/bin/env python
# -*- coding: utf8 -*-

from sqlalchemy import create_engine

#dataBaseDirectory = 'mysql+pymysql://root:utfpr8@localhost/picadel'

class ConnectionWithDataBase(object):
	count = 0
	def __init__ (self, laboratoryName, dataBaseDirectory):
		if ConnectionWithDataBase.count == 0:
			self.laboratoryName = laboratoryName
			self.dataBase = create_engine(dataBaseDirectory)
			ConnectionWithDataBase.count = 1


	def setLaboratoryName(self, labratoryName):
		self.laboratoryName = laboratoryName


	def getLaboratoryName(self):
		return self.laboratoryName


	def setDataBase(self, dataBaseDirectory):
		self.dataBase = create_engine(dataBaseDirectory)


	def getDataBase(self):
		return self.dataBase


	def ChangeIntToDayOfTheWeek(self, dayOfTheWeek):
		if dayOfTheWeek == 0:
			return 'segunda'

		if dayOfTheWeek == 1:
			return 'terca'
			
		if dayOfTheWeek == 2:
			return 'quarta'
		
		if dayOfTheWeek == 3:
			return 'quinta'
		
		if dayOfTheWeek == 4:
			return 'sexta'
		
		if dayOfTheWeek == 5:
			return 'sabado'
		
		if dayOfTheWeek == 6:
			return 'domingo'


	def AllowEntry(self, securityKey):
		# Se nao for estudante, entrada autorizada
		if not self.IsStudentSecurityKey(securityKey): return True

		# Verifica se a chave é permitida
		if not CheckIfSecurityKeyIsAllowed(securityKey): return False

		# Verifica se existe um horario agendado com base no horario atual
		# do usuario.
		if not self.ExistSchedule(): return False

		return True


	def IsStudentSecurityKey(self, securityKey):
		firstPhrase = 'SELECT U.profession FROM user U, security_key SK '
		middlePhrase = 'WHERE SK.security_key = ' + self.ChangeStringToDataBaseCommand(securityKey) + ' AND U.profession = "estudante" '
		lastPhrase = 'AND SK.id = U.security_key_id'

		command = firstPhrase + middlePhrase + lastPhrase
		if not self.ResultCommand(command): return False

		return True


	def ExistSchedule(self):
		command = "SELECT WEEKDAY(CURDATE());"
		currentDayOfTheWeek = self.ChangeIntToDayOfTheWeek(self.ResultCommand(command))
		command = "SELECT CURRENT_TIME()"
		currentTime = self.ResultCommand(command)

		laboratoryCondition = 'L.name = ' + self.getLaboratoryName()
		startTimeCondition = self.ChangeStringToDataBaseCommand(currentTime) + ' >= S.start '
		endTimeCondition = self.ChangeStringToDataBaseCommand(currentTime) + ' <= S.end '
		dayOfTheWeekCondition = 'S.day_of_the_week = ' + self.ChangeStringToDataBaseCommand(currentDayOfTheWeek)
		
		firstPhrase = 'SELECT * FROM schedule S, laboratory L '
		middlePhrase = 'WHERE L.id = S.laboratory_id AND ' + laboratoryCondition + " AND " + startTimeCondition + ' AND ' + endTimeCondition + ' AND ' + dayOfTheWeekCondition
		command = firstPhrase + middlePhrase

		if not self.ResultCommand(command): return False

		return True


	def ResultCommand(self, command):
		with db.connect() as con:
			result = con.executa(command)
			return result.fetchone()[0]


	def ChangeStringToDataBaseCommand(self, phrase):
		return '"' + phrase + '"'


	def CheckIfSecurityKeyIsAllowed(self, securityKey):
		laboratoryCondition = 'L.name = ' + self.ChangeStringToDataBaseCommand(self.getLaboratoryName())
		securityKeyCondition = 'SK.security_key = ' + self.ChangeStringToDataBaseCommand(securityKey)

		firstPhrase = 'SELECT U.name FROM laboratory L, permission P, user U, security_key SK '
		middlePhrase = 'WHERE ' + laboratoryCondition + ' AND ' + securityKeyCondition + ' '
		lastPhrase = 'AND L.id = P.laboratory_id AND U.id = P.user_id AND SK.id = U.security_key_id'

		command = firstPhrase + middlePhrase + lastPhrase

		if not self.ResultCommand(command): return False

		return True