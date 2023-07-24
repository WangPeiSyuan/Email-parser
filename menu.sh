#!/bin/bash
# A menu driven shell script sample template 
## ----------------------------------
# Step #1: Define variables
# ----------------------------------
RED='\033[0;41;30m'
STD='\033[0;0;39m'
 
# ----------------------------------
# Step #2: User defined function
# ----------------------------------
pause(){
  read -p "Press [Enter] key to continue..." fackEnterKey
}

one(){
	python3 /var/www/soc/checkMbox.py
    pause
}
 
two(){
	python3 /var/www/soc/checkDB.py
    pause
}

three(){
	python3 /var/www/soc/checkCompare.py
    pause
} 

four(){
	python3 /var/www/soc/updateDB.py
	pause
}
five(){
	python3 /var/www/soc/compare_schoolnet.py
	pause
}
 
# function to display menus
show_menus() {
	clear
	echo "~~~~~~~~~~~~~~~~~~~~~"	
	echo " M A I N - M E N U"
	echo "~~~~~~~~~~~~~~~~~~~~~"
	echo "1. Check MailBOX: 查看 mailbox 7天內信件"
	echo "2. Check DataBase: 查看 DB 14天內的信件"
	echo "3. Compare Mbox VS.DB: 查看 mailbox 中的信件有沒有 insert 進 DB"
	echo "4. Update school net DB: 更新網段資料表"
	echo "5. Compare school net DB VS. SNMG: 比對現有網段資料與SNMG DB"
	echo "6. Exit"
}
read_options(){
	local choice
	read -p "Enter choice [ 1 - 6] " choice
	case $choice in
		1) one ;;
		2) two ;;
		3) three ;;
		4) four ;;
		5) five ;;
		6) exit 0;;
		*) echo -e "${RED}Error...${STD}" && sleep 2
	esac
}
 
# ----------------------------------------------
# Step #3: Trap CTRL+C, CTRL+Z and quit singles
# ----------------------------------------------
trap '' SIGINT SIGQUIT SIGTSTP
 
# -----------------------------------
# Step #4: Main logic - infinite loop
# ------------------------------------
while true
do 
	show_menus
	read_options
done
