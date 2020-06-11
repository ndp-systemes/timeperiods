TimePeriods
===========

A Python lib intended to handle operation on time periods (ie periods from one `datetime.datetime` to another).

It includes simple set operation like intersection and union.

## Models

This lib mainly include two classe :

### `TimePeriod`

Describes an immutable period, having

* `begin` (`datetime.datetime`) : the beginning of the period (included)
* `end` (`datetime.datetime`) : the end of the period
* `|` (or `+`) : operator returning the union of two `TimePeriod`
* `&` : operation returning the intersection of two `TimePeriod`

### `TimePeriodSet`
 
A set of `TimePeriod` usable as an iterable, and indexable, with


* `periods` : the list of contained `TimePeriod`
* `|` (or `+`) : operator returning the union of all `TimePeriod` in two `TimePeriodSet`, or the union of a `TimePeriodSet` and a `TimePeriod`
* `&` : operator returning all the intersections between the `TimePeriod` of two `TimePeriodSet`, or a `TimePeriodSet` and a single `TimePeriod`

## Exceptions

### InvalidPeriodException

Raised only when trying to create an incoherent `TimePeriod`, ie one in which the beginning is equal or later than the end.

### SeparatePeriodsException

Raised when an operation has been made between two `TimePeriod` without any intersection.

## Features to implement

None yet. If you think one feature is missing, fill free to open a ticket.
