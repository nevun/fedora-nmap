#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/nmap/Sanity/simple-functionality-test
#   Description: Simple functionality test, local port scanning.
#   Author: Karel Srot <ksrot@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2010 Red Hat, Inc. All rights reserved.
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

# Include rhts environment
. /usr/bin/rhts-environment.sh
. /usr/share/beakerlib/beakerlib.sh

PACKAGE="nmap"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        rlRun "TmpDir=\`mktemp -d\`" 0 "Creating tmp directory"
	rlIsRHEL 4 5 && rlRun "chcon -t tmpfs_t $TmpDir" 0 "Changing SELinux context to allow nmap to write to $TmpDir"
        rlRun "pushd $TmpDir"
    rlPhaseEnd

    rlPhaseStartTest
        rlRun "nmap localhost -p- 2>&1 > myscan.nmap" 0 "Perform nmap scan"
        rlAssertExists "myscan.nmap"
	rlRun "lsof -i4 -P | grep '(LISTEN)' > lsof.out" 0 "Checking open ports with lsof -i4"
	if grep -q ':22 (LISTEN)' lsof.out; then
		rlRun "egrep '22/tcp\\W+open\\W+ssh' myscan.nmap" 0 "Checking if ssh has been found"
	fi
	if grep -q ':25 (LISTEN)' lsof.out; then
		rlRun "egrep '25/tcp\\W+open\\W+smtp' myscan.nmap" 0 "Checking if smtp daemon has been found"
	fi
	if grep -q ':631 (LISTEN)' lsof.out; then
		rlRun "egrep '631/tcp\\W+open\\W+ipp' myscan.nmap" 0 "Checking if cups/ipp has been found"
	fi

	if grep -q ':111 (LISTEN)' lsof.out; then
		rlRun "egrep '111/tcp\\W+open\\W+rpcbind' myscan.nmap" 0 "Checking if portmap/rpcbind has been found"
	fi
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
