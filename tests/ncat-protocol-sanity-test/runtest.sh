#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/nmap/Sanity/ncat-protocol-sanity-test
#   Description: Test all supported protocols of ncat, like tcp, udp, ...
#   Author: Patrik Kis <pkis@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2012 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/bin/rhts-environment.sh
. /usr/share/beakerlib/beakerlib.sh

PACKAGE="nmap"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        rlRun "modprobe sctp"
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlIsRHEL 4 5 && rlRun "chcon -t tmpfs_t $TmpDir" 0 \
                "Changing SELinux context to allow nmap to write to $TmpDir"
        rlRun "cp *exp $TmpDir" 0 "Copying expect scripts to working directory"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

    rlPhaseStartTest "ncat acts as tcp server (Listen mode)"
        rlRun "tcpdump -pnnli lo port 6666 > tcpdump-tcp.out &" 0 "Run tcpdump"
        TCPDUMPPID=$!; echo TCPDUMPPID=$TCPDUMPPID
        sleep 2
        rlRun "./tcpsrv.exp > ncat-server-tcp.out &"
        NCATPID=$!; echo NCATPID=$NCATPID
        rlRun "rlWaitForSocket -p $NCATPID 6666 -d 0.5"
        rlRun "./tcpclt.exp > ncat-client-tcp.out"
        sleep 3
        rlRun "kill -9 $NCATPID" 0,1 "Making sure the ncat is dead"
        rlRun "kill -9 $TCPDUMPPID" 0,1 "Making sure the tcpdump is dead"
        sleep 1
        cat tcpdump-tcp.out
        rlAssertGrep "127.0.0.1.6666.*\[S" tcpdump-tcp.out
        rlAssertGrep "127.0.0.1.6666.*\[P" tcpdump-tcp.out
        rlAssertGrep "127.0.0.1.6666.*\[F" tcpdump-tcp.out
        rlAssertEquals "Vefify that there were two PUSH packet sent" \
                2 `grep "127.0.0.1.6666.*\[P" tcpdump-tcp.out |wc -l`
        cat ncat-server-tcp.out
        rlAssertGrep "ClientSend" ncat-server-tcp.out
        cat ncat-client-tcp.out
        rlAssertGrep "ServerSend" ncat-client-tcp.out
    rlPhaseEnd

    rlPhaseStartTest "ncat acts as SCTP server (Listen mode)"
        # SCTP does not support half-open connection so it has to be tested with expect
        # otherwise the parties initiate connection close immediately after all input read
        rlRun "tcpdump -pnnli lo port 6666 > tcpdump-sctp.out &" 0 "Run tcpdump"
        TCPDUMPPID=$!; echo TCPDUMPPID=$TCPDUMPPID
        sleep 2
        rlRun "./srv.exp > ncat-server-sctp.out &"
        NCATPID=$!; echo NCATPID=$NCATPID
        rlRun "rlWaitForSocket -p $NCATPID 6666 -d 0.5"
        rlRun "./clt.exp > ncat-client-sctp.out"
        sleep 3
        rlRun "kill -9 $NCATPID" 0,1 "Making sure the ncat is dead"
        rlRun "kill -9 $TCPDUMPPID" 0,1 "Making sure the tcpdump is dead"
        sleep 1
        cat tcpdump-sctp.out
        rlAssertGrep "127.0.0.1.6666.*sctp.*\[INIT" tcpdump-sctp.out
        rlAssertGrep "127.0.0.1.6666.*sctp.*\[COOKIE" tcpdump-sctp.out
        rlAssertGrep "127.0.0.1.6666.*sctp.*\[SHUTDOWN" tcpdump-sctp.out
        rlAssertEquals "Vefify that there were two DATA sctp packet sent" \
                2 `grep "127.0.0.1.6666.*sctp.*\[DATA\]" tcpdump-sctp.out |wc -l`
        cat ncat-server-sctp.out
        rlAssertGrep "ClientSend" ncat-server-sctp.out
        cat ncat-client-sctp.out
        rlAssertGrep "ServerSend" ncat-client-sctp.out
    rlPhaseEnd

    rlPhaseStartTest "ncat acts as UDP server (Listen mode)"
        rlRun "tcpdump -pnnli lo port 6666 > tcpdump-udp.out &" 0 "Run tcpdump"
        TCPDUMPPID=$!; echo TCPDUMPPID=$TCPDUMPPID
        sleep 2
        rlRun "./udpsrv.exp >ncat-server-udp.out &"
        NCATPID=$!; echo NCATPID=$NCATPID
        sleep 2
        rlRun "./udpclt.exp >ncat-client-udp.out &"
        NCATCLNTPID=$!; echo NCATPID=$NCATCLNTPID
        sleep 2
        rlRun "kill -9 $NCATPID $NCATCLNTPID" 0,1 "Making sure the ncat is dead"
        rlRun "kill -9 $TCPDUMPPID" 0,1 "Making sure the tcpdump is dead"
        sleep 2
        cat tcpdump-udp.out
        rlAssertGrep "127.0.0.1.*>.*127.0.0.1.6666.*UDP" tcpdump-udp.out
        rlAssertGrep "127.0.0.1.6666.*>.*127.0.0.1..*UDP" tcpdump-udp.out
        rlAssertEquals "Vefify that there were two UDP packet sent" \
                2 `wc -l tcpdump-udp.out`
        cat ncat-server-udp.out
        rlAssertGrep "ClientSend" ncat-server-udp.out
        cat ncat-client-udp.out
        rlAssertGrep "ServerSend" ncat-client-udp.out
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
