#!/usr/bin/perl
#
# ////////////////////////////////////////////////////////////////////////// #
# �ե�����᡼�顼 formmailer
# 
# Copyright (c) 2002 Takahiro Nishigaki <takahiro@ahref.org>
# 
# http://www.ahref.org/
#
# $Id: formmailer.cgi,v 1.15 2002/11/12 19:49:00 nishiyan Exp $
#
# ---------------------------------------
# ��AHREF(�������������)��ꤪ�Τ餻��
# ---------------------------------------
# AHREF�Ǥϡ�
# �ɤ����Ƥ⼫�Ϥ�CGI�����֤Ǥ��ʤ����Τ����CGI������֥����ӥ��䡢 
# ���Ȥ��Υ����С��Ǥ�CGI�����Ĥ���Ƥ��ʤ����Τ���� CGIư���ݾڤ�
# AHREF�ۥ��ƥ��󥰥����ӥ��ʤɤ⤴�Ѱդ������Ƥ���ޤ���
# �����ڤˤ��䤤��碌����������
# 
# CGI������ԥ����ӥ�
# http://www.ahref.org/cgidaikou.html
# AHREF�ۥ��ƥ��󥰥����ӥ�
# http://www.ahref.org/hosting.html
#
# �������ư��� 1.14 -> 1.15
# formmailer���Ϥ������ܤΤ�ɽ�������å�
# ���ԤΤʤ����Ϥǥơ��֥뤬�ΤӤ��Զ�罤��
# �����԰��ȼ�ư�ֿ��᡼��η�̾���̡��ǵ�������褦�ˤ���
# ��ǧ���̤�Ф��Ф��ʤ�Ƚ����桼�����Υե��������ϤǹԤ���褦�ˤ�����
# qmail��Return-Path����
# sendmail�ѥ��Υ����å���ǽ
# ////////////////////////////////////////////////////////////////////////// #

# ------------------------
#      �桼��������
# ------------------------
# �����ȥ��HTMLɽ���ѡ�
$title = "���䤤��碌";

# �᡼���̾�ʴ����԰��ѡ�
$subject_admin = "���䤤��碌���Ȥɤ��ޤ�����";

# �᡼���̾�ʼ�ư�ֿ��᡼���ѡ�
$subject_return = "���䤤��碌���꤬�Ȥ��������ޤ���";

# �᡼����������ʣ�������ǽ�� �����㡧@mailto = ('xxx@xxx.xxx','zzz@zzz.zzz');
@mailto = ('infot@tate.jp');

# ������Υڡ����������URL
$backurl = './index.html';

# ɬ�ܹ��� form��name�����ʵ����㡧@indispensable_var=('email','��̾��');��
@indispensable_var = ();

# Ⱦ�ѿ���(0-9��-) form��name�����ʵ����㡧@hankakusuuzicheck_var=('����','FAX');��
@hankakusuuzicheck_var = ();

# Ⱦ�ѹ���(a-zA-Z0-9��-)form��name�����ʵ����㡧@hankakucheck_var=('����','FAX');��
@hankakucheck_var = ();

# Ⱦ�ѥ������ʤ����ѥ������ʤ��Ѵ�����ʤ�1
$chk_h2z = 1;

# ��ǧ���̤�ɽ��������������������ʤ�1
$chk_direct = 0;

# ���Ϥ��줿���ܤΤ�ɽ������������ʤ�1
$chk_onlyvisible = 0;

# �����С���qmail�ξ���1 (�᡼����������qmail�Ѥ�Return-Path���꤬�ʤ���ޤ�)
$isqmail = 0;

# ���Υ�����ץȤ�̾��
$myfile = "formmailer.cgi";

# sendmail�Υѥ�
$sendmail = 'c:\sendm\sendmane.exe'';

# ���ꥵ���Ȱʳ�����Υ���������ػߤ��롣
# �ʵ����㡧$limit_url = 'http://www.ahref.org/cgi/formmailer/';��
$limit_url = '';

# ------------------------
#    ��ư�ֿ��᡼��
# ------------------------
$chk_returnmail = 1;	# 1 = ��ư�ֿ��᡼���ͭ���� 0 = ̵��

$returnmail = 'email';	# ��ư�ֿ���λ��ꡣForm��name�����ʼ�ư�ֿ��᡼��̵�����Ǥ�᡼��κ��пͤȤ��ƻȤ��ޤ�����

$atena = '��̾��';		# ��̾�λ��ꡣForm��name����

$atenakei = '��';		# ��̾�ˤĤ���ɾ�

$mail_from = '';		# ��ư�ֿ��᡼��κ��пͤȤʤ�̾�����ʤ����@mailto�κǽ�Υ��ɥ쥹�����пͤȤʤ롣�ʵ����㡧$mail_from = 'WEB�ޥ����� <xxx@xxxx.xxx>';��

$reptyto = '';			# ��ư�ֿ��᡼����ֿ����REPLY-TO�ˡ��ʤ����@mailto�κǽ�Υ��ɥ쥹�����пͤȤʤ롣�ʵ����㡧$reptyto = 'WEB�ޥ����� <xxx@xxxx.xxx>';��


# ------------------------
#   ��ǧ���̤��Խ�
# ------------------------

# ��ǧ�ڡ��������ȥ�
$kakunintitle = $title;

# ��ǧ�ڡ�����ʸ��
$kakunin = "<br><br>�ʲ������Ƥ򤴳�ǧ�ξ�<br>�����ܥ���򲡤��Ƥ���������";

# ������λ���ʸ��
$thankstext=
"
<br><br>
<div align=\"center\">
<font color=\"#000000\"><b>������λ!!</b></font>
<br><br>
���꤬�Ȥ��������ޤ���<br>
���Ƥ��ǧ�ξ塢�Ǥ��������ޤ˸��ֻ��������ޤ���
<br><br><br><br>
<a href=\"$backurl\">���</a>
</div>
";

# ------------------------
#   �᡼��ʸ�̤��Խ�
# ------------------------

# �᡼����ʸ�ξ���
$mailheader = 
'���꤬�Ȥ��������ޤ���
�������Ƥϰʲ��Τ褦�ˤʤäƤ���ޤ���
----------------------------------------
';

# �᡼����ʸ�β���
$mailfooter=
'
----------------------------------------
Powere by FORMMAILER http://www.ahref.org/
';


# ------------------------
#  �桼�������ꤳ���ޤ�
# ------------------------


# ////////////////////////////////////////////////////////////////////////// #
# �����ƥ���������

require "./jcode.pl";
require './mimew.pl';

$version = 'formmailer http://www.ahref.org/';

# ��������å�
&error("sendmail�Υѥ�������������ޤ���<br>$sendmail") unless -x $sendmail;

# ���ꥵ���Ȱʳ�����Υ���������ػ�
&limit_access($limit_url);

# �ե����फ�������
if ($buffer eq ''){
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		}
	else {
		$buffer = $ENV{'QUERY_STRING'};
		}
}
@pairs = split(/&/,$buffer);

#Ⱦ�ѥ������ʤ����ѥ������ʤ��Ѵ�
if($chk_h2z){
	$buffer =~ tr/+/ /;
	$buffer =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
	$kcode=&jcode::getcode(\$buffer);
}
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
	$name =~ tr/+/ /;
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;

	#ʸ���������Ѵ���Ⱦ�ѥ������ʤ����ѥ������ʤ��Ѵ���
	if($chk_h2z){
		&jcode::convert(\$name,euc,"$kcode","z");
		&jcode::convert(\$value,euc,"$kcode","z");
	}else{
		&jcode::convert(\$name,euc);
		&jcode::convert(\$value,euc);
	}
	push(@FORM_N,$name);
	push(@FORM_V,$value);
	$FORM{$name} = $value;
	
	# �ե����फ��Υǡ�������HTML��Ǻ�ɽ�����뤿��Υ���̵����
	$name = &plantext2html($name);
	$value= &plantext2html($value);
	push(@FORM_FN,$name);
	push(@FORM_FV,$value);
}
# ��ư�ֿ��᡼�밸������
$returnmail_to = $FORM{$returnmail};

# ��ư�ֿ��᡼��ͭ�����Τߥ᡼�륢�ɥ쥹�����å�
if($chk_returnmail){
	&emailcheck($returnmail_to);
}

# �᡼��������Ԥ�����
if(&emailcheck($returnmail_to,"noerror")){
	$mailfrom = $returnmail_to;
}elsif(!&emailcheck($returnmail_to,"noerror")){
	$mailfrom = 'nobody@'.$ENV{'SERVER_NAME'};
}

#���ϥ����å�
&datacheck(@indispensable_var);		# ɬ�ܹ���@indispensable_var�������
&hankakucheck(@hankakucheck_var);		# Ⱦ��@hankakucheck_var�������
&hankakusuuzicheck(@hankakusuuzicheck_var);		# Ⱦ�ѿ���@hankakusuuzicheck_var�������

&envetc;


# ////////////////////////////////////////////////////////////////////////// #
# �ᥤ�������������

if($FORM{'formmailer_check'}||$chk_direct eq "1"){
	foreach(@mailto){
		# �����Ԥإ᡼������
		&mailsend($_,1);
	}
	# ��ư�ֿ��᡼��
	if ($chk_returnmail && $returnmail){
		&mailsend($returnmail_to,0);
	}
	&thanks;
}else{
	&kakunin;
}

exit;
# �ᥤ����������

# ////////////////////////////////////////////////////////////////////////// #
# �ե������ɬ�ܻ�������å�
sub datacheck{

	foreach (@_){
		if (!$FORM{$_}){&error("$_�������Ʋ�������");}
	}

}
# ////////////////////////////////////////////////////////////////////////// #
# �ե������Ⱦ�ѥ����å�
sub hankakucheck{

	foreach (@_){
		&hankaku_check($FORM{$_},$_);
	}

}
# ////////////////////////////////////////////////////////////////////////// #
# �ե������Ⱦ�ѿ��������å�
sub hankakusuuzicheck{

	foreach (@_){
		&hankakusuuzi_check($FORM{$_},$_);
	}

}
# ////////////////////////////////////////////////////////////////////////// #
sub kakunin{

# ��ǧ�ڡ����ơ��֥�ο�
my $tdcolor = "#000099";
my $font = "#ffffff";
my $tdcolor_left = "#ccecf4";
my $font_left = "#000000";
my $tdcolor_right = "#ffffff";
my $font_right = "#000000";

&htmlheader;

print <<EOF;
<div align="center">$kakunin
<form method="post" action="$myfile">
<input type=hidden name="formmailer_check" value="sendmail">
<table border=0 cellpadding=3 cellspacing=3 align="center">
<tr><td align="center" colspan="2" bgcolor=\"$tdcolor\"><font color=\"$font\">$kakunintitle</font></td></tr>
EOF


foreach (0..$#FORM_FN) {

	next if $FORM_N[$_] eq "formmailer_check";

	next if $chk_onlyvisible && !$FORM_FV[$_];
	$FORM_FV[($_)] =~ s/\n/<br>/g;
	
	print "<input type=hidden name=\"$FORM_FN[($_)]\" value=\"$FORM_FV[($_)]\">\n";
	print "<tr><td bgcolor=\"$tdcolor_left\"><font color=\"$font_left\">$FORM_FN[($_)] </font><br></td>";
	print "<td bgcolor=\"$tdcolor_right\"><font color=\"$font_right\">$FORM_FV[($_)] </font></td></tr>\n";
	print "</td></tr>\n";

}


print "</table><br><br>";
print "<input type=\"submit\" value=\"����������\"> ";
print "<INPUT type=\"button\" value=\"cancel\" onClick=\'history.back();\'>";
print "</form><div>";

&htmlfooter;

}

# ////////////////////////////////////////////////////////////////////////// #
sub mailsend {
	my $body;
	my $toadmincheck = $_[1];
	if(!$mail_from){$mail_from = $mailto[0];}
	if(!$reptyto){$reptyto = $mailto[0];}
	if(!$toadmincheck){
		# ��̾
		if($atena){
			foreach (0..$#FORM_N) {
				if ($FORM_N[$_] eq $atena && $FORM_V[$_]){
					$body.="$FORM_V[$_]$atenakei\n\n";
				}
			}
		}
		# �᡼��إå���
		$body.="$mailheader";
	}

	foreach (0..$#FORM_N) {
		next if $FORM_N[$_] eq "formmailer_check";
		next if $chk_onlyvisible && !$FORM_FV[$_];
		$FORM_V[($_)] =~ s/<br>//g;
		$body.="$FORM_N[$_] = $FORM_V[$_]\n";
	}

	if(!$toadmincheck){
		# �᡼��եå���
		$body.="$mailfooter";
	}
	
	if($toadmincheck){
		$body.="\n";
		$body.="----------------------------------------\n";
		$body.="DATE              : $nowdate\n";
		$body.="SERVER_NAME       : $ENV{'SERVER_NAME'}\n";
		$body.="HTTP_USER_AGENT   : $ENV{'HTTP_USER_AGENT'}\n";
		$body.="REMOTE_HOST       : $host\n";
		$body.="REMOTE_ADDR       : $ENV{'REMOTE_ADDR'}\n";
		$body.="----------------------------------------\n";
	}
	
	
	# �᡼������
	if($toadmincheck){
		&jmailsend($sendmail,$_[0],$subject_admin,$body,$mailfrom,$mailfrom,$version,$mailto[0]);
	}else{
		# ��ư�ֿ��᡼��
		&jmailsend($sendmail,$_[0],$subject_return,$body,$mail_from,$reptyto,$version,$mailto[0]);
	}
	
}

# ////////////////////////////////////////////////////////////////////////// #
sub thanks {

	&htmlheader;
	print $thankstext;
	&htmlfooter;

}

# ////////////////////////////////////////////////////////////////////////// #
sub jmailsend{

	my $sendmail=$_[0];
	my $to=$_[1];
	my $subject=$_[2];
	my $body=$_[3];
	my $from=$_[4];
	my $replyto=$_[5];
	my $xmailer=$_[6];
	my $returnpath = $_[7];

	#̤���ϥ��顼
	if (!$sendmail){return 0;}
	if (!$to){return 0;}
	if (!$from){return 0;}
	
	# to,replyto,returnpath�ϥ᡼�륢�ɥ쥹�Τ����
	my $to_m = &getmail($to);
	$replyto = &getmail($replyto);
	$returnpath = &getmail($returnpath);

	#sendmail�ε�ư
	if($isqmail){
		#qmail�����С�
		open(MAIL,"| $sendmail -f $returnpath $to") || return undef;
	}else{
		open(MAIL,"| $sendmail $to") || return undef;
	}

	#��̾����ʸ��JIS���Ѵ�
	&jcode::convert(\$subject, "jis");
	&jcode::convert(\$body, "jis");

	#�᡼��HEADER���
	print MAIL "Return-Path: $returnpath\n" if $returnpath;
	print MAIL "X-Mailer: $xmailer\n" if $xmailer;
	print MAIL "Reply-To: $replyto\n" if $replyto;
	print MAIL &mimeencode("To: $to\n");
	print MAIL &mimeencode("From: $from\n");
	print MAIL &mimeencode("Subject: $subject\n");
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "Content-Type: text/plain\; charset=\"ISO-2022-JP\"\n\n";

	#�᡼����ʸ���
	print MAIL $body;

	close(MAIL);
	return 1;
}


# ////////////////////////////////////////////////////////////////////////// #
sub getmail{
	my $mail = shift;
	my $mail_regex = q{([\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)\@([\w|\!\#\$\%\'\(\)\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)};
	if($mail =~ /$mail_regex/o){
		$mail =~ s/($mail_regex)(.*)/$1/go;		# �᡼�륢�ɥ쥹�κǸ�ʹߤ���
		$mail =~ s/(.*)[^\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+($mail_regex)/$2/go;		# �᡼�륢�ɥ쥹�ޤǤ���
	}
	return $mail;
}

# ////////////////////////////////////////////////////////////////////////// #
sub envetc{

	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$mon++;
	$sec = "0$sec" if $sec < 10;
	$min = "0$min" if $min < 10;
	$hour = "0$hour" if $hour < 10;
	$mday = "0$mday" if $mday < 10;
	$mon = "0$mon" if $mon < 10;
	$year = $year + 1900;
	$week = ("Sun","Mon","Tue","Wed","Thu","Fri","Sat")[$wday];
	$nowdate = "$year/$mon/$mday($week) $hour:$min:$sec";
	$host = $ENV{'REMOTE_HOST'};
	$address = $ENV{'REMOTE_ADDR'};
	if ($host eq $address) {
		$host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $address;
	}
}

# ////////////////////////////////////////////////////////////////////////// #
sub htmlheader{

print <<EOF;
Content-Type: text/html; charset=EUC-JP

<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=EUC-JP">
<title>$title</title>
</head>
<body bgcolor="#FFFFFF">
EOF
}

# ////////////////////////////////////////////////////////////////////////// #
sub htmlfooter{

# ///////////////////////////////////////////////////////////////// #
# �ڽ��ס����ɽ���ˤĤ���
# 
# AHREF �ե꡼CGI�ǤϤ����Ѥˤ��������ɽ���򤪴ꤤ���Ƥ���ޤ���
# ���ɽ����Ϥ����ˤϤ������������������
# �������ɽ���ˤĤ���
# http://www.ahref.org/cgityosaku.html
# ///////////////////////////////////////////////////////////////// #

print <<EOF;
<br><br>
<table width="640" border="0" cellspacing="0" cellpadding="2" align="center">
  <tr align="center">
	<td><font size=-2 color=#999999>&copy;2003 FORMMAILER <a href="http://www.ahref.org/">ahref.org</a></font></td>
  </tr>
</table>
</div>
</body>
</html>
EOF
}


# ////////////////////////////////////////////////////////////////////////// #
# E-mail�����å�
sub emailcheck{
	if($_[0] !~ /^[\.!#%&\-_0-9a-z]+\@[!#%&\-_0-9a-z]+(\.[!#%&\-_0-9a-z]+)+$/i){
		if(!$_[1]){
			&error('�᡼�륢�ɥ쥹���������������Ʋ�������');
		}else{
			return undef;
		}
	}
	return 1;
}
# ////////////////////////////////////////////////////////////////////////// #
# Ⱦ�ѱѿ������å�
sub hankaku_check{
	if($_[0] =~ /[^\w\-]/){
		&error("$_[1]��Ⱦ�ѱѿ��ǵ������Ʋ�������");
	}
}
# ////////////////////////////////////////////////////////////////////////// #
# Ⱦ�ѿ��������å�
sub hankakusuuzi_check{
	if($_[0] =~ /[^0-9\-]/){
		&error("$_[1]��Ⱦ�ѿ����ǵ������Ʋ�������");
	}
}
# ////////////////////////////////////////////////////////////////////////// #
# ¾�����Ȥ���Υ����������ӽ�
# ////////////////////////////////////////////////////////////////////////// #
sub limit_access{
	my $ref_url = shift;
	if ($ref_url) {
		if (!$ENV{'HTTP_REFERER'} || $ENV{'HTTP_REFERER'} !~ /^$ref_url/ ) {
			&error("�����ʥ��������Ǥ���");
		}
	}
}
# HTML�ü�ʸ�����������ס����Ԥ�<br>���Ѵ�
sub plantext2html{
	my $text = shift;
	if ($text){
		$text =~ s/&/&amp;/g;
		$text =~ s/</&lt;/g;
		$text =~ s/>/&gt;/g;
		$text =~ s/\"/&quot;/g;

	}
	return $text;
}
# <br>��\n���᤹�ʥ᡼���ѡ�
sub html2plantext{
	my $text = shift;
	$text =~ s/<br>/\n/g;
	return $text;
}
# ////////////////////////////////////////////////////////////////////////// #
# ���顼
# ////////////////////////////////////////////////////////////////////////// #
sub error{
	my $error = shift;

print "Content-type: text/html\n\n";
print <<"EOF";	
<HTML>
<HEAD>
<meta http-equiv="content-type" content="text/html;charset=EUC-JP">
<TITLE>error</TITLE>
</HEAD>
<BODY BGCOLOR="#808080" LINK="#000066" VLINK="#666666">
<TABLE BORDER=1 WIDTH=450 HEIGHT=170 bgcolor=FFFFFF align="center">
  <TR valign="top"> 
	<TD> 
	  <table border=0 width="99%">
		<tr align="center"> 
		  <td bgcolor="#cc3333" width="80%"> <b><font size="+1" color="#FFFFFF">���顼</font></b> 
		  </td>
		</tr>
	  </table>
	  <blockquote><br>
	  $error<br><br>
	  <div align="center">
	  <a href="javascript:history.back();"><b>���</b></a></div></blockquote></TD>
  </TR>
</TABLE>
</BODY>
</HTML>

EOF
exit;

}
