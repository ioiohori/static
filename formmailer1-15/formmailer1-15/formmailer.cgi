#!/usr/bin/perl
#
# ////////////////////////////////////////////////////////////////////////// #
# フォームメーラー formmailer
# 
# Copyright (c) 2002 Takahiro Nishigaki <takahiro@ahref.org>
# 
# http://www.ahref.org/
#
# $Id: formmailer.cgi,v 1.15 2002/11/12 19:49:00 nishiyan Exp $
#
# ---------------------------------------
# ※AHREF(エーエイチレフ)よりお知らせ※
# ---------------------------------------
# AHREFでは、
# どうしても自力でCGIを設置できない方のためにCGI代行設置サービスや、 
# お使いのサーバーではCGIが許可されていない方のために CGI動作保証の
# AHREFホスティングサービスなどもご用意いたしております。
# お気軽にお問い合わせください。
# 
# CGI設置代行サービス
# http://www.ahref.org/cgidaikou.html
# AHREFホスティングサービス
# http://www.ahref.org/hosting.html
#
# 修正内容一覧 1.14 -> 1.15
# formmailer入力した項目のみ表示チェック
# 改行のない入力でテーブルがのびる不具合修正
# 管理者宛と自動返信メールの件名を別々で記入するようにした
# 確認画面を出す出さない判定ををユーザーのフォーム入力で行えるようにした。
# qmail用Return-Path設定
# sendmailパスのチェック機能
# ////////////////////////////////////////////////////////////////////////// #

# ------------------------
#      ユーザー設定
# ------------------------
# タイトル（HTML表示用）
$title = "お問い合わせ";

# メール件名（管理者宛用）
$subject_admin = "お問い合わせがとどきました。";

# メール件名（自動返信メール用）
$subject_return = "お問い合わせありがとうございました";

# メールの送信先（複数指定可能） 記入例：@mailto = ('xxx@xxx.xxx','zzz@zzz.zzz');
@mailto = ('infot@tate.jp');

# 送信後のページから戻るURL
$backurl = './index.html';

# 必須項目 formのnameを記入（記入例：@indispensable_var=('email','お名前');）
@indispensable_var = ();

# 半角数字(0-9と-) formのnameを記入（記入例：@hankakusuuzicheck_var=('電話','FAX');）
@hankakusuuzicheck_var = ();

# 半角項目(a-zA-Z0-9と-)formのnameを記入（記入例：@hankakucheck_var=('電話','FAX');）
@hankakucheck_var = ();

# 半角カタカナを全角カタカナに変換するなら1
$chk_h2z = 1;

# 確認画面を表示せずすぐに送信するなら1
$chk_direct = 0;

# 入力された項目のみ表示・送信するなら1
$chk_onlyvisible = 0;

# サーバーがqmailの場合は1 (メール送信時にqmail用のReturn-Path設定がなされます)
$isqmail = 0;

# このスクリプトの名前
$myfile = "formmailer.cgi";

# sendmailのパス
$sendmail = 'c:\sendm\sendmane.exe'';

# 指定サイト以外からのアクセスを禁止する。
# （記入例：$limit_url = 'http://www.ahref.org/cgi/formmailer/';）
$limit_url = '';

# ------------------------
#    自動返信メール
# ------------------------
$chk_returnmail = 1;	# 1 = 自動返信メールを有効。 0 = 無効

$returnmail = 'email';	# 自動返信先の指定。Formのnameを記入（自動返信メール無効時でもメールの差出人として使われます。）

$atena = 'お名前';		# 宛名の指定。Formのnameを記入

$atenakei = '様';		# 宛名につける敬称

$mail_from = '';		# 自動返信メールの差出人となる名前、なければ@mailtoの最初のアドレスが差出人となる。（記入例：$mail_from = 'WEBマスター <xxx@xxxx.xxx>';）

$reptyto = '';			# 自動返信メールの返信先（REPLY-TO）、なければ@mailtoの最初のアドレスが差出人となる。（記入例：$reptyto = 'WEBマスター <xxx@xxxx.xxx>';）


# ------------------------
#   確認画面の編集
# ------------------------

# 確認ページタイトル
$kakunintitle = $title;

# 確認ページの文章
$kakunin = "<br><br>以下の内容をご確認の上<br>送信ボタンを押してください。";

# 送信完了後の文章
$thankstext=
"
<br><br>
<div align=\"center\">
<font color=\"#000000\"><b>送信完了!!</b></font>
<br><br>
ありがとうございます。<br>
内容を確認の上、できるだけ早急に御返事いたします。
<br><br><br><br>
<a href=\"$backurl\">戻る</a>
</div>
";

# ------------------------
#   メール文面の編集
# ------------------------

# メール本文の上部
$mailheader = 
'ありがとうございます。
送信内容は以下のようになっております。
----------------------------------------
';

# メール本文の下部
$mailfooter=
'
----------------------------------------
Powere by FORMMAILER http://www.ahref.org/
';


# ------------------------
#  ユーザー設定ここまで
# ------------------------


# ////////////////////////////////////////////////////////////////////////// #
# システム初期設定部

require "./jcode.pl";
require './mimew.pl';

$version = 'formmailer http://www.ahref.org/';

# 設定チェック
&error("sendmailのパスが正しくありません。<br>$sendmail") unless -x $sendmail;

# 指定サイト以外からのアクセスを禁止
&limit_access($limit_url);

# フォームからの入力
if ($buffer eq ''){
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		}
	else {
		$buffer = $ENV{'QUERY_STRING'};
		}
}
@pairs = split(/&/,$buffer);

#半角カタカナを全角カタカナに変換
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

	#文字コード変換（半角カタカナを全角カタカナに変換）
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
	
	# フォームからのデーターをHTML上で再表示するためのタグ無効化
	$name = &plantext2html($name);
	$value= &plantext2html($value);
	push(@FORM_FN,$name);
	push(@FORM_FV,$value);
}
# 自動返信メール宛先を取得
$returnmail_to = $FORM{$returnmail};

# 自動返信メール有効時のみメールアドレスチェック
if($chk_returnmail){
	&emailcheck($returnmail_to);
}

# メールの送信者を設定
if(&emailcheck($returnmail_to,"noerror")){
	$mailfrom = $returnmail_to;
}elsif(!&emailcheck($returnmail_to,"noerror")){
	$mailfrom = 'nobody@'.$ENV{'SERVER_NAME'};
}

#入力チェック
&datacheck(@indispensable_var);		# 必須項目@indispensable_varがあれば
&hankakucheck(@hankakucheck_var);		# 半角@hankakucheck_varがあれば
&hankakusuuzicheck(@hankakusuuzicheck_var);		# 半角数字@hankakusuuzicheck_varがあれば

&envetc;


# ////////////////////////////////////////////////////////////////////////// #
# メイン処理ここから

if($FORM{'formmailer_check'}||$chk_direct eq "1"){
	foreach(@mailto){
		# 管理者へメール送信
		&mailsend($_,1);
	}
	# 自動返信メール
	if ($chk_returnmail && $returnmail){
		&mailsend($returnmail_to,0);
	}
	&thanks;
}else{
	&kakunin;
}

exit;
# メイン処理おわり

# ////////////////////////////////////////////////////////////////////////// #
# フォームの必須事項チェック
sub datacheck{

	foreach (@_){
		if (!$FORM{$_}){&error("$_を記入して下さい。");}
	}

}
# ////////////////////////////////////////////////////////////////////////// #
# フォームの半角チェック
sub hankakucheck{

	foreach (@_){
		&hankaku_check($FORM{$_},$_);
	}

}
# ////////////////////////////////////////////////////////////////////////// #
# フォームの半角数字チェック
sub hankakusuuzicheck{

	foreach (@_){
		&hankakusuuzi_check($FORM{$_},$_);
	}

}
# ////////////////////////////////////////////////////////////////////////// #
sub kakunin{

# 確認ページテーブルの色
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
print "<input type=\"submit\" value=\"　送　信　\"> ";
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
		# 宛名
		if($atena){
			foreach (0..$#FORM_N) {
				if ($FORM_N[$_] eq $atena && $FORM_V[$_]){
					$body.="$FORM_V[$_]$atenakei\n\n";
				}
			}
		}
		# メールヘッダー
		$body.="$mailheader";
	}

	foreach (0..$#FORM_N) {
		next if $FORM_N[$_] eq "formmailer_check";
		next if $chk_onlyvisible && !$FORM_FV[$_];
		$FORM_V[($_)] =~ s/<br>//g;
		$body.="$FORM_N[$_] = $FORM_V[$_]\n";
	}

	if(!$toadmincheck){
		# メールフッター
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
	
	
	# メール送信
	if($toadmincheck){
		&jmailsend($sendmail,$_[0],$subject_admin,$body,$mailfrom,$mailfrom,$version,$mailto[0]);
	}else{
		# 自動返信メール
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

	#未入力エラー
	if (!$sendmail){return 0;}
	if (!$to){return 0;}
	if (!$from){return 0;}
	
	# to,replyto,returnpathはメールアドレスのみ抽出
	my $to_m = &getmail($to);
	$replyto = &getmail($replyto);
	$returnpath = &getmail($returnpath);

	#sendmailの起動
	if($isqmail){
		#qmailサーバー
		open(MAIL,"| $sendmail -f $returnpath $to") || return undef;
	}else{
		open(MAIL,"| $sendmail $to") || return undef;
	}

	#件名、本文をJISに変換
	&jcode::convert(\$subject, "jis");
	&jcode::convert(\$body, "jis");

	#メールHEADER定義
	print MAIL "Return-Path: $returnpath\n" if $returnpath;
	print MAIL "X-Mailer: $xmailer\n" if $xmailer;
	print MAIL "Reply-To: $replyto\n" if $replyto;
	print MAIL &mimeencode("To: $to\n");
	print MAIL &mimeencode("From: $from\n");
	print MAIL &mimeencode("Subject: $subject\n");
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "Content-Type: text/plain\; charset=\"ISO-2022-JP\"\n\n";

	#メール本文定義
	print MAIL $body;

	close(MAIL);
	return 1;
}


# ////////////////////////////////////////////////////////////////////////// #
sub getmail{
	my $mail = shift;
	my $mail_regex = q{([\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)\@([\w|\!\#\$\%\'\(\)\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+)};
	if($mail =~ /$mail_regex/o){
		$mail =~ s/($mail_regex)(.*)/$1/go;		# メールアドレスの最後以降を削除
		$mail =~ s/(.*)[^\w|\!\#\$\%\'\=\-\^\`\\\|\~\[\{\]\}\+\*\.\?\/]+($mail_regex)/$2/go;		# メールアドレスまでを削除
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
# 【重要】著作権表示について
# 
# AHREF フリーCGIではご使用にあたり著作権表示をお願いしております。
# 著作権表示をはずすにはこちらをご覧ください。
# ■著作権非表示について
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
# E-mailチェック
sub emailcheck{
	if($_[0] !~ /^[\.!#%&\-_0-9a-z]+\@[!#%&\-_0-9a-z]+(\.[!#%&\-_0-9a-z]+)+$/i){
		if(!$_[1]){
			&error('メールアドレスを正しく記入して下さい。');
		}else{
			return undef;
		}
	}
	return 1;
}
# ////////////////////////////////////////////////////////////////////////// #
# 半角英数チェック
sub hankaku_check{
	if($_[0] =~ /[^\w\-]/){
		&error("$_[1]は半角英数で記入して下さい。");
	}
}
# ////////////////////////////////////////////////////////////////////////// #
# 半角数字チェック
sub hankakusuuzi_check{
	if($_[0] =~ /[^0-9\-]/){
		&error("$_[1]は半角数字で記入して下さい。");
	}
}
# ////////////////////////////////////////////////////////////////////////// #
# 他サイトからのアクセスを排除
# ////////////////////////////////////////////////////////////////////////// #
sub limit_access{
	my $ref_url = shift;
	if ($ref_url) {
		if (!$ENV{'HTTP_REFERER'} || $ENV{'HTTP_REFERER'} !~ /^$ref_url/ ) {
			&error("不正なアクセスです。");
		}
	}
}
# HTML特殊文字エスケープ＆改行を<br>に変換
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
# <br>を\nに戻す（メール用）
sub html2plantext{
	my $text = shift;
	$text =~ s/<br>/\n/g;
	return $text;
}
# ////////////////////////////////////////////////////////////////////////// #
# エラー
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
		  <td bgcolor="#cc3333" width="80%"> <b><font size="+1" color="#FFFFFF">エラー</font></b> 
		  </td>
		</tr>
	  </table>
	  <blockquote><br>
	  $error<br><br>
	  <div align="center">
	  <a href="javascript:history.back();"><b>戻る</b></a></div></blockquote></TD>
  </TR>
</TABLE>
</BODY>
</HTML>

EOF
exit;

}
