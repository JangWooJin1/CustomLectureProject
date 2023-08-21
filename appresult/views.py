from django.shortcuts import render
import copy

# Create your views here.
# nCr의 모든 경우의수를 출력하는 함수
def Combination(self, lst, tmp, n, r, index, depth):
    newtmp = copy.deepcopy(tmp)
    if r == 0:
        if self.checkCredits(newtmp):
            self.comb.append(newtmp)
    elif depth < n:
        newtmp[index] = lst[depth]
        self.Combination(lst, newtmp, n, r - 1, index + 1, depth + 1)
        self.Combination(lst, newtmp, n, r, index, depth + 1)

# myLecture와 allTimeTable를 형성하는 함수
def makeTimeTable(self):
    n = len(self.myLecture)
    # myLecture에 있는 강의를 가지고 allTimeTable채우기(이 부분을 수정하여 확장가능)

    #가장 큰 학점 in 장바구니
    maxCredit = max(L[0].totalCredits for L in self.myLecture)

    #최소 r값 구하기 - 내가 들어야하는 최소 학점수 / maxCredit을
    r = self.Credits[0] // maxCredit

    while r <= n:  ####################### r탈출 조건 더 생각해보기 ###################################
        self.Combination(list(range(n)), [-1] * r, n, r, 0, 0)
        r += 1

    # [[0,1], [0,1,2]]
    for lst in self.comb:
        size = 1
        for i in lst:
            size *= len(self.myLecture[i])  # 전체경우의수조정
        self.totalSize += size

    TimeTable = []
    Times = []
    isvalid = []
    size = []

    # 위에서 결정된 전체경우의수를 가지고 allTimeTable,Times,isvalid 크기 결정
    for i in range(len(self.comb)):
        TimeTable.append([])
        Times.append([])
        isvalid.append([])
        size.append([])

    for n, lst in enumerate(self.comb):
        size[n] = 1
        split = []
        for i in lst:
            size[n] *= len(self.myLecture[i])  # 전체경우의수조정
            split.append(len(self.myLecture[i]))

        for i in range(size[n]):
            TimeTable[n].append([])
            Times[n].append([])
            isvalid[n].append(True)

        for index, i in enumerate(lst):
            self.fillTimeTable(self.myLecture[i], TimeTable[n], Times[n], isvalid[n], split, index)

    for i in range(len(self.comb)):
        self.allTimeTable += TimeTable[i]
        self.Times += Times[i]
        self.isvalid += isvalid[i]
    self.professors = list(self.professors)

#allTimeTable내용 채우는 함수각 그룹에서 조합할수있는 모든 경우의수 구하기 )
def fillTimeTable(self,lst,TimeTable, Times, isvalid,split, index):
    totalsplit = 1 #기준점
    for k in range(index+1,len(split)):
      totalsplit *= split[k]

    i=0 #매개변수 lst(=myLecture의 원소)의 인덱스
    for j,tmp in enumerate(TimeTable):
      if isvalid[j]: #유효한 시간표만 강의추가작업
        self.professors.add(lst[i].professor)
        tmp.append(lst[i])  #lst의 i번째 강의를 allTimeTable시간표에 추가
        self.checkCollision(lst[i],j,Times,isvalid) #추가후 해당 시간표의 유효성 검사

      #기준점에 도달하면 i값 업데이트
      if (j+1) % totalsplit == 0:
        i+=1
      if i >= len(lst):
        i=0

  #강의시간 충돌을 확인하는 함수 월1.0-3.0
def checkCollision(self, L, index, Times, isvalid):
    Tmps = []     #강의L의 시간을 임시 저장[[요일,시작시간,종료시간]]
    time = L.time #문자열 슬라이싱에 사용할 강의L의 시간
    i = 0         #문자열 슬라이싱 기준 인덱스값
    day = ""      #요일
    start = 0.0   #시작시간
    end = 0.0     #종료시간
    last = False  #반복문종료를 판단하는 변수
    while not last:
      day = time[0:1] #time에서 요일 추출
      time = time[1:] #요일 추출후 time값 조정

      i = time.find('-')        #-을 기준으로
      start = float(time[0:i])  #time에서 시작시간 추출
      time = time[i+1:]         #시작시간 추출후 time값 조정

      i = time.find('_')        #_을 기준으로
      if i == -1:               #_이 없다 == time문자열의 마지막
        last=True               #반복문 변수값 업데이트
        i = len(time)           #기준값 업데이트
      end = float(time[0:i])    #time에서 종료시간 추출
      time = time[i+1:]         #종료시간 추출후 time값 조정

      Tmps.append([day,start,end])  #추출한 요일,시작시간,종료시간을 Tmps에 추가

    #기존시간표(Times[index])와 현재 강의L의 시간표(Tmps)의 시간 충돌을 확인
    for i in Times[index]:
      for j in Tmps:
        if i[0] == j[0]:  #먼저 요일이 동일여부 확인
          if j[1] <= i[2] and j[2] >= i[1]: #강의L의 시작시간 < 기존강의 종료시간 and 강의L의 종료시간 > 기존강의 시작시간
            isvalid[index] = False   #위 조건을 모두 만족하면 시간이 충돌한다는 의미 => 유효하지않은 시간표
            return #해당 시간표가 이미 유효하지않다는 것을 확인하면 뒤에 남은 작업 처리 불필요 => 함수종료(시간단축)
    Times[index]+=Tmps   #시간충돌을 하지않는다면 현재 강의L 시간표를 기존 시간표에 합치기
