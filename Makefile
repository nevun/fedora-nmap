# Makefile for source rpm: nmap
# $Id$
NAME := nmap
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
