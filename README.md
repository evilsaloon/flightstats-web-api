# Flightstats Web App API Reference

## Table of Contents
- [Table of Contents (you're here!)](#table-of-contents)
- [Glossary](#glossary)
- [JSON API](#json-api)
    - [Airport Arrivals / Departures](#airport-arrivals--departures)
    - [Past and Upcoming Flights](#past-and-upcoming-flights)
    - [Flight Tracking API](#flight-tracking-api)
    - [Random Flight](#random-flight)
    - [Flight Information from ID](#flight-information-from-id)
    - [Airline / Airport Search](#airline--airport-search)
    - [Airport Code Validator](#airport-code-validator)
    - [Airport Information](#airport-information)
    - [Airport Search (POST)](#airport-search-post)
    - [Home Page Search (POST)](#home-page-search-post)
- ["Fake" API](#fake-api)
	- [window.__data](#window__data)
		- [Airport Delays](#airport-delays)
		- [Extended Flight Details](#extended-flight-details)
		- [On Time Performance Rating](#on-time-performance-rating)
	- [\_\_NEXT_DATA\_\_](#__next_data__)
		- [Flight Tracker](#flight-tracker)
		- [Route Search](#route-search)
		- [Flight Tracker Map](#flight-tracker-map)
		- [Flight Tracker Stops](#flight-tracker-stops)

## Glossary:

- "Observed Time Period" (or OTP for short): A period of 7 days, which spans the current day and 3 days before and after the current day. This is the time period that the API returns data for. Historical data is not displayed to unauthenticated (or registered "Standard" plan) users in order to drive subscription sales.

## JSON API

These are all of the methods I managed to find that are used by the flightstats v2 web app. Querying these endpoints is as simple as sending a GET or POST request. 

No authentication is required for any of these methods at the time of writing. However, for some endpoints, the "rqid" (request ID) field is mandatory.

Because some endpoints can return a LOT of data, all JSON examples in this document are abbreviated. Press the "Extended example" links to see the raw JSON files.

Base URL: https://www.flightstats.com/v2

### Airport Arrivals / Departures

GET URL: /api-next/flight-tracker/:type/:airport/:year/:month/:day/:startHour?carrierCode=:code&numHours=:hours

Get arrival/departure information for a certain airport. This endpoint only returns data in the OTP in chunks of a maximum size of 12 hours.

Parameters:

- type: Return arrivals or departures for a certain airport. Must be "arr" or "dep" respectively. Mandatory.
- airport: Must be an IATA 3 letter or an ICAO 4 letter airport code. For example: "SCE". Mandatory.
- year: Year to lookup. Must be year with century. For example: "2022". Mandatory.
- month: Month to lookup. Can be zero-padded or not. For example: "2" or "02". Mandatory.
- day: Day to lookup. Can be zero-padded or not. For example: "3" or "03". Mandatory.
- startHour: The hour at which the lookup starts. Meant to make lookups easier in the web app, as to avoid overwhelming the user with information (for example, the time period 00:00-06:00 would have a startHour of 0). Can be any integer number from 0 to 23. Mandatory.
- carrierCode: Carrier (airline) IATA code. Used for limiting the results to only one airline/carrier. Optional.
- hours: Number of hours to return data for. Can be any integer from 1 to 12. However, the sum of startHour and hours must never exceed 24.

Example URL: https://www.flightstats.com/v2/api-next/flight-tracker/dep/SCE/2022/8/6/0?numHours=12 - Lists departures at SCE airport on 2022-08-06 from hours 00:00 to 12:00.

Returns:
- If unsuccessful: Status code 500 in the headers and `{"data":{},"error":{"message":"Request failed with status code 500","code":500}}` in the body.
- If successful: dictionary with header and list of flights.
	- [Extended Example.](/jsons/flighttracker_departures.json)
	- Abbreviated example:
```
{
	"data": {
		"header": {
			"date": "06-Aug-2022",
			"dateMDY": "Aug-06-2022",
			"title": "(SCE) University Park Airport Departures",
			"mobileTitle": "SCE Departures",
			"departureAirport": {
				"fs": "SCE",
				"iata": "SCE",
				"icao": "KUNV",
				"name": "University Park Airport",
				"city": "State College",
				"state": "PA",
				"country": "US",
				"active": true,
				"classification": 4,
				"timeZoneRegionName": "America/New_York"
			}
		},
		"destOriginTitle": "Destination",
		"flights": [{
			"sortTime": "2022-08-06T10:28:00.000Z",
			"departureTime": {
				"timeAMPM": "6:28AM",
				"time24": "06:28"
			},
			"arrivalTime": {
				"timeAMPM": "7:26AM",
				"time24": "07:26"
			},
			"carrier": {
				"fs": "AA",
				"name": "American Airlines",
				"flightNumber": "6095"
			},
			"operatedBy": "Operated by Piedmont Airlines on behalf of American Airlines",
			"url": "/flight-tracker/AA/6095?year=2022&month=8&date=6&flightId=1103982191",
			"airport": {
				"fs": "PHL",
				"city": "Philadelphia"
			}
		}]
	}
}
```

### Past and Upcoming Flights

GET URL: /api-next/flight-tracker/other-days/:carrierCode/:number

Get past and upcoming flight information in the OTP for a flight number.

Parameters:

- carrierCode: Carrier (airline) IATA code. Mandatory.
- number: Flight number. Mandatory.

Example URL: https://www.flightstats.com/v2/api-next/flight-tracker/other-days/UA/3867 - Lists all UA 3867 flights in the OTP.

Returns:
- If unsuccessful: `{"data":""}` in the body.
- If successful: Dictionary with list of flights every day.
	- [Extended Example.](/jsons/flighttracker_otherdays.json)
	- Abbreviated example:
```
{
	"data": [{
		"date1": "05-Aug",
		"date2": "Aug-05",
		"day": "Friday",
		"year": "2022",
		"flights": [{
			"arrivalAirport": {
				"city": "Chicago",
				"fs": "ORD",
				"iata": "ORD",
				"name": "O'Hare International Airport",
				"state": "IL",
				"country": "US"
			},
			"arrivalTime": "6:55",
			"arrivalTimeAmPm": "PM",
			"arrivalTime24": "18:55",
			"arrivalTimezone": "CDT",
			"departureAirport": {
				"city": "State College",
				"fs": "SCE",
				"iata": "SCE",
				"name": "University Park Airport",
				"state": "PA",
				"country": "US"
			},
			"departureTime": "5:59",
			"departureTimeAmPm": "PM",
			"departureTime24": "17:59",
			"departureTimezone": "EDT",
			"url": "/flight-tracker/UA/3867?year=2022&month=08&date=05&flightId=1103904930",
			"sortTime": "2022-08-05T21:59:00.000Z"
		}]
	}]
}
```

### Flight Tracking API

GET URL: /api-next/flight-tracker/:carrierCode/:number/:year/:month/:day

Flight tracking info for a certain flight for a certain day within the OTP.

Parameters:

- carrierCode: Carrier (airline) IATA code. Mandatory.
- year: Year to lookup. Must be year with century. For example: "2022". Mandatory.
- month: Month to lookup. Can be zero-padded or not. For example: "2" or "02". Mandatory.
- day: Day to lookup. Can be zero-padded or not. For example: "3" or "03". Mandatory.

Example URL: https://www.flightstats.com/v2/api-next/flight-tracker/UA/3867/2022/8/8 - Lists flight tracking data for all all UA 3867 flights on 2022-08-08

Returns:
- If unsuccessful: `{}` in the body.
- If successful: Dictionary with notes about flight (cancellation status, departure/arrival gate) if available, positional tracking information if available, departure/arrival airport, etc.
	- [Extended Example.](/jsons/flighttracker_departed.json)
	- Abbreviated example:
```
{
	"data": {
		"flightId": 1104374082,
		"flightNote": {
			"final": false,
			"canceled": false,
			"hasDepartedGate": false,
			"hasDepartedRunway": false,
			"landed": false,
			"message": "Tracking will begin after departure",
			"messageCode": "S",
			"pastExpectedTakeOff": false,
			"tracking": false,
			"hasPositions": false,
			"trackingUnavailable": false,
			"phase": null,
			"hasActualRunwayDepartureTime": false,
			"hasActualGateDepartureTime": false
		},
		"isTracking": false,
		"isLanded": false,
		"isScheduled": true,
		"sortTime": "2022-08-08T21:59:00.000Z",
		"schedule": {
			"scheduledDeparture": "2022-08-08T17:59:00.000",
			"scheduledDepartureUTC": "2022-08-08T21:59:00.000Z",
			"estimatedActualDepartureRunway": false,
			"estimatedActualDepartureTitle": "Estimated",
			"estimatedActualDeparture": "2022-08-08T17:59:00.000",
			"estimatedActualDepartureUTC": "2022-08-08T21:59:00.000Z",
			"scheduledArrival": "2022-08-08T18:55:00.000",
			"scheduledArrivalUTC": "2022-08-08T23:55:00.000Z",
			"estimatedActualArrivalRunway": false,
			"estimatedActualArrivalTitle": "Estimated",
			"estimatedActualArrival": "2022-08-08T18:55:00.000",
			"estimatedActualArrivalUTC": "2022-08-08T23:55:00.000Z",
			"graphXAxis": {
				"dep": "2022-08-08T17:59:00.000",
				"depUTC": "2022-08-08T21:59:00.000Z",
				"arr": "2022-08-08T18:55:00.000",
				"arrUTC": "2022-08-08T23:55:00.000Z"
			}
		},
		"status": {
			"statusCode": "S",
			"status": "Scheduled",
			"color": "green",
			"statusDescription": "On time",
			"delay": {
				"departure": {
					"minutes": 0
				},
				"arrival": {
					"minutes": 0
				}
			},
			"delayStatus": {
				"wording": "On time",
				"minutes": 0
			},
			"lastUpdatedText": "Status Last Updated More Than 3 Hours Ago",
			"diverted": false
		},
		"resultHeader": {
			"statusDescription": "On time",
			"carrier": {
				"name": "United Airlines",
				"fs": "UA"
			},
			"flightNumber": "3867",
			"status": "Scheduled",
			"diverted": false,
			"color": "green",
			"departureAirportFS": "SCE",
			"arrivalAirportFS": "ORD",
			"divertedAirport": null
		},
		"ticketHeader": {
			"carrier": {
				"name": "United Airlines",
				"fs": "UA"
			},
			"flightNumber": "3867"
		},
		"operatedBy": "Operated by Air Wisconsin on behalf of United Airlines",
		"departureAirport": {
			"fs": "SCE",
			"iata": "SCE",
			"name": "University Park Airport",
			"city": "State College",
			"state": "PA",
			"country": "US",
			"timeZoneRegionName": "America/New_York",
			"regionName": "North America",
			"gate": "B",
			"terminal": null,
			"times": {
				"scheduled": {
					"time": "5:59",
					"ampm": "PM",
					"time24": "17:59",
					"timezone": "EDT"
				},
				"estimatedActual": {
					"title": "Estimated",
					"time": "5:59",
					"ampm": "PM",
					"time24": "17:59",
					"runway": false,
					"timezone": "EDT"
				}
			},
			"date": "2022-08-08T17:59:00.000"
		},
		"arrivalAirport": {
			"fs": "ORD",
			"iata": "ORD",
			"name": "O'Hare International Airport",
			"city": "Chicago",
			"state": "IL",
			"country": "US",
			"timeZoneRegionName": "America/Chicago",
			"regionName": "North America",
			"gate": "F6",
			"terminal": "2",
			"baggage": "2",
			"times": {
				"scheduled": {
					"time": "6:55",
					"ampm": "PM",
					"time24": "18:55",
					"timezone": "CDT"
				},
				"estimatedActual": {
					"title": "Estimated",
					"time": "6:55",
					"ampm": "PM",
					"time24": "18:55",
					"runway": false,
					"timezone": "CDT"
				}
			},
			"date": "2022-08-08T18:55:00.000"
		},
		"divertedAirport": null,
		"additionalFlightInfo": {
			"equipment": {
				"iata": "CR2",
				"name": "Canadair (Bombardier) Regional Jet 200",
				"title": "Actual"
			},
			"flightDuration": "1h 56m"
		},
		"codeshares": [],
		"positional": {
			"departureAirportCode": "SCE",
			"arrivalAirportCode": "ORD",
			"divertedAirportCode": null,
			"flexFlightStatus": "S",
			"flexTrack": {
				"flightId": 1104374082,
				"carrierFsCode": "ZW",
				"flightNumber": "3867",
				"tailNumber": "N429AW",
				"departureAirportFsCode": "SCE",
				"arrivalAirportFsCode": "ORD",
				"departureDate": {
					"dateUtc": "2022-08-08T21:59:00.000Z",
					"dateLocal": "2022-08-08T17:59:00.000"
				},
				"equipment": "CR2",
				"bearing": 281.7803912486057,
				"positions": [],
				"irregularOperations": [],
				"fleetAircraftId": 63158
			}
		},
		"flightState": "currentDatePreFlight"
	}
}
```

### Random Flight

GET URL: /api-next/random-flight

Get random flight in flightstats' system.

No parameters.

Example URL: https://www.flightstats.com/v2/api-next/random-flight

Returns: 
- Dictionary with flight and some minimal information.
	- [Extended Example.](/jsons/randomflight.json)
	- Abbreviated example:
```
{
    "data": [{
        "_index": "flights_2022_08_09",
        "_type": "flight",
        "_id": "1104376832_UU975",
        "_score": 6.786226,
        "_source": {
            "flightId": 1104376832,
            "hubUrl": "http://hub.iad.prod.flightstats.io/channel/ProcessedFlightHistory/2022/08/08/16/59/09/274/YzstfK",
            "classification": 0.3333333333333333,
            "keywords": "UU 975 RUN CDG",
            "lastUpdated": "2022-08-08T16:58:54Z",
            "creator": "Innovata",
            "creationDate": "2022-08-05T13:47-0700",
            "carrier": "UU",
            "carrierIata": "UU",
            "carrierIcao": "REU",
            "carrierName": "Air Austral",
            "flightNumber": "975",
            "status": "ACTIVE",
            "codeshares": [{
                "carrier": "AF",
                "trafficRestriction": "",
                "flightNumber": "5011"
            }],
            "departureAirport": "RUN",
            "departureTimeZone": "Indian/Reunion",
            "departureAirportName": "Reunion Roland Garros Airport",
            "departureAirportCity": "Saint Denis de la Reunion",
            "arrivalAirport": "CDG",
            "arrivalTimeZone": "Europe/Paris",
            "arrivalAirportName": "Charles de Gaulle Airport",
            "arrivalAirportCity": "Paris",
            "departureDateTime": "2022-08-08T20:15+0400",
            "publishedDeparture": "2022-08-08T20:15+0400",
            "scheduledGateDeparture": "2022-08-08T20:15+0400",
            "arrivalDateTime": "2022-08-09T05:30+0200",
            "publishedArrival": "2022-08-09T05:30+0200",
            "scheduledGateArrival": "2022-08-09T05:30+0200",
            "arrivalTerminal": "2C",
            "scheduledEquipment": "77W",
            "recordStatus": "active",
            "id": null,
            "wetlease": null,
            "tailNumber": "F-OREU",
            "departure": null,
            "arrival": null,
            "delayMinutesDeparture": 15,
            "delayMinutesArrival": null,
            "estimatedGateDeparture": "2022-08-08T20:30+0400",
            "actualGateDeparture": "2022-08-08T20:30+0400",
            "scheduledRunwayDeparture": null,
            "estimatedRunwayDeparture": "2022-08-08T20:40+0400",
            "actualRunwayDeparture": "2022-08-08T20:40+0400",
            "estimatedGateArrival": "2022-08-09T05:21+0200",
            "actualGateArrival": null,
            "scheduledRunwayArrival": null,
            "estimatedRunwayArrival": "2022-08-09T05:12+0200",
            "actualRunwayArrival": null,
            "departureGate": null,
            "arrivalGate": null,
            "baggage": null,
            "actualEquipment": "77W",
            "actualEquipmentIcao": "B77W"
        }
    }]
}
```

### Flight Information from ID

GET URL: /api-next/flick/:flightId?guid=:guid&rqid=:guid

Get detailed information about a flight from its internal flightId.

Parameters:

- flightId: Internal flight ID. Mandatory.
- guid: Arbitrary ID. Mandatory.
- rqid: Random alphanumeric string 2-13 characters in length. Mandatory.


Example URL: https://www.flightstats.com/v2/api-next/flick/1104374141?guid=evilsalooner&rqid=evilsaloon

Returns:
- If rqid or guid isn't provided: Status code 405 in the headers and `{"data":{},"error":{"message":"Request failed with status code 405","code":405}}` in the body.
- If unsuccessful: Status code 500 in the headers and `{"data":{},"error":{"message":"Request failed with status code 500","code":500}}` in the body.
- If successful: Similar information to the [Flight Tracking API](#flight-tracking-api) endpoint.
	- [Extended Example.](/jsons/flick.json)
	- Abbreviated example:
```
{
    "data": {
        "responseTime": 1659990035,
        "flightId": "1104374141",
        "operatedByFlightNum": "3954",
        "statusCode": "A",
        "statusName": "DEPARTED",
        "statusColor": "#4B9142",
        "statusAppendKey": "onTime",
        "statusAppend": "ON-TIME",
        "flightEquipmentIata": "CR2",
        "flightEquipmentName": "Canadair (Bombardier) Regional Jet",
        "airports": {
            "departure": {
                "fsCode": "ORD",
                "name": "O'Hare International Airport",
                "city": "Chicago",
                "stateCode": "IL",
                "countryCode": "US",
                "countryName": "United States",
                "localTime": "2022-08-08T15:20:35.456",
                "latitude": 41.976912,
                "longitude": -87.904876,
                "elevationFt": 668,
                "conditions": "Cloudy",
                "temperatureCelsius": 23,
                "conditionIcon": "cloud@2x.png"
            },
            "arrival": {
                "fsCode": "SCE",
                "name": "University Park Airport",
                "city": "State College",
                "stateCode": "PA",
                "countryCode": "US",
                "countryName": "United States",
                "localTime": "2022-08-08T16:20:35.456",
                "latitude": 40.853721,
                "longitude": -77.848228,
                "elevationFt": 1239,
                "conditions": "Cloudy",
                "temperatureCelsius": 30,
                "conditionIcon": "cloud@2x.png"
            },
            "diverted": {
                "fsCode": "",
                "name": "",
                "city": "",
                "stateCode": "",
                "countryCode": "",
                "countryName": "",
                "localTime": "",
                "latitude": "",
                "longitude": "",
                "elevationFt": ""
            }
        },
        "bearing": 97.48334528268376,
        "heading": 98.35372292603024,
        "flightStatus": "A",
        "operationalTimes": {
            "isActualDeparture": true,
            "utc": {
                "departureTime": 1659986940,
                "departureTimeString": "2022-08-08T19:29:00.000Z",
                "arrivalTime": 1659992700,
                "arrivalTimeString": "2022-08-08T21:05:00.000Z",
                "actualRunwayArrivalTime": null,
                "actualRunwayArrivalTimeString": null,
                "actualRunwayDepartureTime": 1659988380,
                "actualRunwayDepartureTimeString": "2022-08-08T19:53:00.000Z"
            },
            "local": {
                "departureTime": 1659968940,
                "departureTimeString": "2022-08-08T14:29:00.000",
                "arrivalTime": 1659978300,
                "arrivalTimeString": "2022-08-08T17:05:00.000",
                "actualRunwayArrivalTime": null,
                "actualRunwayArrivalTimeString": null,
                "actualRunwayDepartureTime": 1659970380,
                "actualRunwayDepartureTimeString": "2022-08-08T14:53:00.000"
            }
        },
        "positions": ["CUT OUT FOR SPACE REASONS"],
        "miniTracker": {
            "statusName": "DEPARTED",
            "flightStatusCode": "A",
            "utcDepartureTime": 1659986940,
            "localDepartureTime": 1659968940,
            "localDepartureTimeString": "2022-08-08T14:29:00.000",
            "isActualDepartureTime": false,
            "utcArrivalTime": 1659992700,
            "localArrivalTime": 1659978300,
            "localArrivalTimeString": "2022-08-08T17:05:00.000",
            "isActualArrivalTime": false,
            "utcActualRunwayArrivalTime": null,
            "utcActualRunwayDepartureTime": 1659988380,
            "totalKilometers": 847.3507492876795,
            "arrivalAirport": "SCE",
            "departureAirport": "ORD",
            "kilometersFromDeparture": 215.71343326775437,
            "kilometersToArrival": 631.788114573287
        }
    }
}
```

### Airline / Airport Search

GET URL: /api-next/search/airline-airport?query=:query&type=:type

Get an airline or airport's code by the name and vice versa.

Parameters:
- query: Search query. Must be URL formatted (ex: %20 instead of space). Mandatory.
- type: Can be either "airline" or "airport". Mandatory.

Example URLs:
- https://www.flightstats.com/v2/api-next/search/airline-airport?query=ua&type=airline - Searches for an airline with the query "ua"
- https://www.flightstats.com/v2/api-next/search/airline-airport?query=sce&type=airport - Searches for an airport with the query "sce"

Returns:
- If unsuccessful: `{"data":[]}` in the body.
- If successful: Dictionary with found airline or airport:
```
{
	"data": [{
		"fs": "UA",
		"name": "United Airlines"
	}, {
		"fs": "UJX",
		"name": "AtlasGlobal UA"
	}, {
		"fs": "HST",
		"name": "UAB Heston Airlines"
	}, {
		"fs": "EK",
		"name": "Emirates"
	}]
}
```
```
{
	"data": [{
		"iata": "SCE",
		"fs": "SCE",
		"name": "University Park Airport"
	}]
}
```

### Airport Code Validator

GET URL: /api/search/airport/:airport?rqid=:rqid

Validates that a code is a valid airport in flightstats' system.

Parameters:

- airport: Must be an IATA 3 letter or an ICAO 4 letter airport code. For example: "SCE". Mandatory.
- rqid: Random alphanumeric string 2-13 characters in length. Mandatory.

Example URL: https://www.flightstats.com/v2/api/search/airport/sce?rqid=evilsaloon - Validates an airport with code "sce"

Returns:
- If rqid is missing: Status code 405 in the headers and `Sorry ¯\_(ツ)_/¯` in the body.
- If unsuccessful: Status code 500 in the headers and `Internal Server Error` in the body.
- If successful: Dictionary with minimal airport data (IATA/ICAO code and full name):
```
{
	"_index": "airports_clio",
	"_type": "airport",
	"_id": "SCE",
	"_version": 9659,
	"found": true,
	"_source": {
		"fs": "SCE",
		"iata": "SCE",
		"icao": "KUNV",
		"name": "University Park Airport",
		"classification": 0.25,
		"city": "State College, PA, US",
		"isActive": "true",
		"cityCode": "SCE",
		"countryCode": "US"
	}
}
```

### Airport Information

GET URL: /api/airport/:airport?rqid=:rqid

Get info about an airport in flightstats' system.

Parameters:

- airport: Must be an IATA 3 letter or an ICAO 4 letter airport code. For example: "SCE". Mandatory.
- rqid: Random alphanumeric string 2-13 characters in length. Mandatory.

Example URL: https://www.flightstats.com/v2/api/airport/SCE?rqid=evilsaloon

Returns:
- If rqid is missing: Status code 405 in the headers and `Sorry ¯\_(ツ)_/¯` in the body.
- If airport not found: Status code 500 in the headers and `{"error":true,"message":"Airport not found"}` in the body.
- If airport code is invalid: Status code 422 in the headers and `{"error":true,"message":"Invalid request for flex"}` in the body.
- If successful: Dictionary consisting of airport details (codes, time), delay index, current and forecast weather.
	- [Extended Example.](/jsons/airportinfo.json)
	- Abbreviated example:
```
{
    "detailsHeader": {
        "code": "SCE",
        "name": "University Park Airport",
        "addressLine2": "State College, US",
        "city": "State College",
        "countryCode": "US",
        "currentDate": "08-Aug-2022",
        "currentTime": "17:30",
        "currentDateTime": "2022-08-08T17:30:37Z",
        "timeZoneRegionName": "America/New_York",
        "currentDateMDY": "Aug-08-2022",
        "currentTimeAMPM": "5:30 PM",
        "stateCode": "PA",
        "timeZone": "EDT",
        "latitude": 40.853721,
        "longitude": -77.848228
    },
    "delayIndex": {
        "observed": true,
        "score": 2.75,
        "status": "Moderate",
        "trend": "Increasing",
        "lastUpdated": "Last updated over an hour ago"
    },
    "currentWeather": {
        "tempF": 84,
        "tempC": 29,
        "wind": {
            "knots": 10,
            "mph": 12,
            "kph": 19
        },
        "direction": 320,
        "visibility": {
            "miles": 10,
            "km": 16
        },
        "hideCurrentWeatherConditionsCard": false,
        "sky": "Broken clouds",
        "icon": "rain"
    },
    "forecastWeather": [{
        "date": "08-Aug-2022",
        "dateMDY": "Aug-08-2022",
        "day1": "Monday",
        "des1": "Mostly sunny. Highs around 80.",
        "icon": "sun",
        "day2": "Tonight",
        "des2": "Mostly cloudy with a chance of showers and thunderstorms this evening, then partly cloudy after midnight. Warm with lows in the lower 70s. Southwest winds 5 to 10 mph. Chance of rain 30 percent.",
        "icon2": "stormy"
    }]
}
```


### Airport Search (POST)

POST URL:  /api/search/airport-search?rqid=:rqid

Search for an airport with specified search string.

JSON: {"value":":value"}

Parameters:

- value: Must be a string. For example: "university%20park". Mandatory.
- rqid: Random alphanumeric string 2-13 characters in length. Mandatory.

Returns: List of airports and their codes. [Extended Example.](/jsons/airportsearch.json)
```
[{
		"_index": "airports_clio",
		"_type": "airport",
		"_id": "SCE",
		"_score": 0,
		"_source": {
			"fs": "SCE",
			"iata": "SCE",
			"icao": "KUNV",
			"name": "University Park Airport",
			"classification": 0.25,
			"city": "State College, PA, US",
			"isActive": "true",
			"cityCode": "SCE",
			"countryCode": "US"
		}
	}
]
```

### Home Page Search (POST)

POST URL: /api/search/structured-search?rqid=:rqid

Searches for flights with certain query.

JSON: {"value":":value"}

Parameters:

- value: Must be a string. For example: "university park". Mandatory.
- rqid: Random alphanumeric string 2-13 characters in length. Mandatory.

Returns: List of flights and detailed info about them. [Extended Example.](/jsons/structuredsearch.json)
```
[{
	"_index": "flights_2022_08_08",
	"_type": "flight",
	"_id": "1104322155_DL3889",
	"_score": 12.90106,
	"_source": {
		"flightId": 1104322155,
		"hubUrl": "http://hub.iad.prod.flightstats.io/channel/ProcessedFlightHistory/2022/08/08/20/17/28/935/zOzaQr",
		"classification": 1,
		"keywords": "DL 3889 SCE DTW",
		"lastUpdated": "2022-08-08T20:17:13Z",
		"creator": "Innovata",
		"creationDate": "2022-08-05T13:20-0700",
		"carrier": "DL",
		"carrierIata": "DL",
		"carrierIcao": "DAL",
		"carrierName": "Delta Air Lines",
		"flightNumber": "3889",
		"status": "ACTIVE",
		"codeshares": [{
				"carrier": "AF",
				"trafficRestriction": "G",
				"flightNumber": "6821"
			},
			{
				"carrier": "KL",
				"trafficRestriction": "A",
				"flightNumber": "7108"
			},
			{
				"carrier": "VS",
				"trafficRestriction": "G",
				"flightNumber": "2477"
			}
		],
		"wetlease": {
			"scheduleText": "/SKYWEST DBA DELTA CONNECTION",
			"carrier": "OO"
		},
		"departureAirport": "SCE",
		"departureTimeZone": "America/New_York",
		"departureAirportName": "University Park Airport",
		"departureAirportCity": "State College",
		"arrivalAirport": "DTW",
		"arrivalTimeZone": "America/New_York",
		"arrivalAirportName": "Detroit Metropolitan Wayne County Airport",
		"arrivalAirportCity": "Detroit",
		"departureDateTime": "2022-08-08T15:53-0400",
		"publishedDeparture": "2022-08-08T15:53-0400",
		"scheduledGateDeparture": "2022-08-08T15:53-0400",
		"arrivalDateTime": "2022-08-08T17:10-0400",
		"publishedArrival": "2022-08-08T17:10-0400",
		"scheduledGateArrival": "2022-08-08T17:10-0400",
		"arrivalTerminal": "M",
		"scheduledEquipment": "CRJ",
		"recordStatus": "active",
		"id": null,
		"tailNumber": "N477CA",
		"departure": null,
		"arrival": null,
		"delayMinutesDeparture": -4,
		"delayMinutesArrival": null,
		"estimatedGateDeparture": "2022-08-08T15:49-0400",
		"actualGateDeparture": "2022-08-08T15:49-0400",
		"scheduledRunwayDeparture": "2022-08-08T16:08-0400",
		"estimatedRunwayDeparture": "2022-08-08T16:06-0400",
		"actualRunwayDeparture": "2022-08-08T16:06-0400",
		"estimatedGateArrival": "2022-08-08T17:14-0400",
		"actualGateArrival": null,
		"scheduledRunwayArrival": "2022-08-08T17:01-0400",
		"estimatedRunwayArrival": "2022-08-08T16:58-0400",
		"actualRunwayArrival": null,
		"departureGate": null,
		"arrivalGate": "C14",
		"baggage": "3",
		"actualEquipment": "CR2",
		"actualEquipmentIcao": "CRJ2"
	}
}]
```

## "Fake" API

This is not a real API. You don't query an endpoint and get a response with JSON. Instead, data on these pages are served as a JS variable that can be extracted.

Data obtained from these pages are probably internal data used by the web app. Because of this, there is a higher risk of these methods not working in the future. You have been warned.

Most of the extra information on these pages has been cut out for space reasons. If you want the full JSON, press the "Extended Example" link to jump to the full file.

### window.__data

Pages in this section have data embedded in a JS variable called "window.__data". window.__data often contains a lot of extra information used internally by the web app.

Here is some Python sample code to extract those data:

```
import httpx
import bs4 
import json

url = "" #put url here
a = httpx.get(url).text
soup = bs4.BeautifulSoup(a, features="lxml")
b = soup.find_all('script')
longest = 0 #window.__data is the longest script tag, so we can extract it that way
out = ""
for item in b:
    if item.get("charset") and item.get("nonce"): #window.__data always has these attributes
        if len(str(item)) > longest:
            longest = len(str(item))
            out = item

data = json.loads(out.contents[0][14:-1]) #json data ready to use 
```

### Airport Delays 

GET URL: https://www.flightstats.com/v2/airport-delays/:region

Get airport delays for all regions, as well as detailed data about one random airport.

Example URL: https://www.flightstats.com/v2/airport-delays/northAmerica

Parameters:
- region: Must be "northAmerica", "europe", "asia", "oceania", "africa", or "southAmerica". Mandatory.

Returns: [Extended Example.](/jsons/airportdelays.json)
```
{
	"App": {
		"AirportDelayMap": {
			"delayIndices": [{
				"name": "Ain Beida Airport",
				"code": "OGX",
				"position": [
					31.916667,
					5.4
				],
				"score": 0,
				"classification": 4,
				"regionName": "africa"
			}],
			"delayObj": {
				"africa": [{
					"name": "Ain Beida Airport",
					"code": "OGX",
					"position": [
						31.916667,
						5.4
					],
					"score": 0,
					"classification": 4,
					"regionName": "africa"
				}],
				"data": {
					"detailsHeader": {
						"code": "ZRH",
						"name": "Zurich Airport",
						"addressLine2": "Zurich, CH",
						"city": "Zurich",
						"countryCode": "CH",
						"currentDate": "10-Aug-2022",
						"currentTime": "18:34",
						"currentDateTime": "2022-08-10T18:34:37Z",
						"timeZoneRegionName": "Europe/Zurich",
						"currentDateMDY": "Aug-10-2022",
						"currentTimeAMPM": "6:34 PM",
						"timeZone": "CEST",
						"latitude": 47.450604,
						"longitude": 8.561746
					},
					"delayIndex": {
						"observed": true,
						"score": 3.75,
						"status": "Significant",
						"trend": "Decreasing",
						"lastUpdated": "Last updated over an hour ago"
					},
					"currentWeather": {
						"tempF": 81,
						"tempC": 27,
						"wind": {
							"knots": 11,
							"mph": 13,
							"kph": 20
						},
						"direction": 80,
						"visibility": {
							"miles": 6,
							"km": 10
						},
						"hideCurrentWeatherConditionsCard": false,
						"icon": null
					},
					"forecastWeather": []
				}
			}

		}
	}
}
```

### Extended Flight Details

GET URL: https://www.flightstats.com/v2/flight-details/:carrierCode/:number

Get extended flight details: Departure and arrival time and gates, full event timeline.

Parameters:
- carrierCode: Carrier (airline) IATA code. Mandatory.
- number: Flight number. Mandatory.

Example URL: https://www.flightstats.com/v2/flight-details/UA/3867

Returns: [Extended Example.](/jsons/flightdetails.json)
```
{
	"App": {
		"SingleFlightTracker": {
			"extendedData": {
				"sortTime": "2022-08-10T21:59:00.000Z",
				"flightId": 1104664029,
				"carrier": {
					"fs": "UA",
					"name": "United Airlines",
					"flightNumber": "3867",
					"iata": "UA",
					"icao": "UAL",
					"active": true,
					"category": "I"
				},
				"codeshares": null,
				"divertedAirport": null,
				"operatedBy": "Operated by Air Wisconsin on behalf of United Airlines",
				"departureTimes": {
					"scheduledGate": {
						"time": "5:59",
						"ampm": "pm",
						"time24": "17:59",
						"timezone": "EDT"
					}
				},
				"arrivalTimes": {
					"scheduledGate": {
						"time": "6:55",
						"ampm": "pm",
						"time24": "18:55",
						"timezone": "CDT"

					}
				},
				"url": "/historical-flight/UA/3867/2022/8/10/1104664029",
				"status": {
					"statusCode": "S",
					"status": "Scheduled",
					"color": "green",
					"statusDescription": "On time"
				},
				"eventTimeline": [{
					"date1": "Aug 10",
					"date2": "10 Aug",
					"utcTime": "12:58",
					"sortTime": "2022-08-10T12:58:39Z",
					"source": "Airline Direct",
					"departureAirportTime": "8:58 am",
					"departureAirportTime24": "08:58",
					"arrivalAirportTime": "7:58 am",
					"arrivalAirportTime24": "07:58",
					"title": "Gate Adjustment",
					"shortTitle": "Gate Adjust",
					"events": [{
						"eventText": "Arrival Gate changed from F22 to F28",
						"noAdjustments": true
					}]
				}]
			},
			"flightState": "currentDatePreFlight",
			"uplines": [],
			"downlines": []
		}
	}
}
```

### On Time Performance Rating

GET URL: https://www.flightstats.com/v2/flight-ontime-performance-rating/:carrierCode/:number

Get on time performance rating for a flight.

Parameters:
- carrierCode: Carrier (airline) IATA code. Mandatory.
- number: Flight number. Mandatory.

Example URL: https://www.flightstats.com/v2/flight-ontime-performance-rating/UA/3867

Returns: [Extended Example.](/jsons/ontimeperformancerating.json)
```
{
	"OnTimePerformance": {
		"error": null,
		"loadAttempts": 1,
		"loading": false,
		"loaded": true,
		"ratings": [{
			"airline": {
				"fs": "UA",
				"iata": "UA",
				"icao": "UAL",
				"name": "United Airlines",
				"active": true,
				"category": "I",
				"flightNumber": "4730"
			},
			"departureAirport": {
				"fs": "SCE",
				"iata": "SCE",
				"icao": "KUNV",
				"name": "University Park Airport",
				"city": "State College",
				"state": "PA",
				"country": "US",
				"active": true,
				"classification": 4,
				"timeZoneRegionName": "America/New_York"
			},
			"arrivalAirport": {
				"fs": "ORD",
				"iata": "ORD",
				"icao": "KORD",
				"name": "O'Hare International Airport",
				"city": "Chicago",
				"state": "IL",
				"country": "US",
				"active": true,
				"classification": 1,
				"timeZoneRegionName": "America/Chicago"
			},
			"flightNumber": "3867",
			"chart": {
				"onTime": 45,
				"late": 1,
				"veryLate": 5,
				"excessive": 8,
				"cancelled": 1,
				"diverted": 1
			},
			"statistics": {
				"totalObservations": 60,
				"delayObservations": 25,
				"codeshares": 60,
				"mean": 47,
				"standardDeviation": 65.4,
				"min": 1,
				"max": 268
			},
			"details": {
				"overall": {
					"stars": 2.7,
					"roundedStars": 2.5,
					"appraisal": "Average",
					"ontimePercent": 75,
					"cumulative": 53,
					"delayMean": 47
				},
				"otp": {
					"stars": 4.6,
					"roundedStars": 4.5,
					"appraisal": "Very Good",
					"ontimePercent": 75,
					"cumulative": 92
				},
				"delayPerformance": {
					"stars": 0.8,
					"roundedStars": 1,
					"appraisal": "Poor",
					"cumulative": 16,
					"delayMean": 47,
					"standardDeviation": 65.4
				}
			},
			"otherStops": [{
				"departureAirport": {
					"fs": "ORD",
					"iata": "ORD",
					"icao": "KORD",
					"name": "O'Hare International Airport",
					"city": "Chicago",
					"state": "IL",
					"country": "US",
					"active": true,
					"classification": 1,
					"timeZoneRegionName": "America/Chicago"
				},
				"arrivalAirport": {
					"fs": "GRR",
					"iata": "GRR",
					"icao": "KGRR",
					"name": "Gerald R. Ford International Airport",
					"city": "Grand Rapids",
					"state": "MI",
					"country": "US",
					"active": true,
					"classification": 3,
					"timeZoneRegionName": "America/New_York"
				},
				"rating": 3.2,
				"appraisal": "Average",
				"roundedStars": 3
			}]
		}]
	}
}
```

### \_\_NEXT_DATA\_\_ 

Data on these pages tends to have a lot less extra information, and mostly contains only what the web app needs to show the user data.

Here is some Python sample code to extract those data:

```
import httpx
import bs4
import json

url = "" #put url here
a = httpx.get(url).text
soup = bs4.BeautifulSoup(a, features = "lxml")
b = soup.find_all('script')
for item in b:
    if not item.get("src") and not item.get("type"): #next data is the only script tag without any src or type attributes
        c = item

data = c.contents[0].split("\n")[1][26:]
```

### Flight Tracker

GET URL: https://www.flightstats.com/v2/flight-tracker/:carrierCode/:number

This page seems to have the same data as the regular JSON API, which is not used by the web app to display information to the user.

Parameters:
- carrierCode: Carrier (airline) IATA code. Mandatory.
- number: Flight number. Mandatory.

Example URL: https://www.flightstats.com/v2/flight-tracker/UA/3867

Returns: [Extended Example.](/jsons/flighttrack.json)
```
{
	"props": {
		"initialState": {
			"flightTracker": {
				"flight": {
					"flightId": 1104812458,
					"flightNote": {
						"final": false,
						"canceled": false,
						"hasDepartedGate": false,
						"hasDepartedRunway": false,
						"landed": false,
						"message": "Tracking will begin after departure",
						"messageCode": "S",
						"pastExpectedTakeOff": false,
						"tracking": false,
						"hasPositions": false,
						"trackingUnavailable": false,
						"phase": null,
						"hasActualRunwayDepartureTime": false,
						"hasActualGateDepartureTime": false
					},
					"isTracking": false,
					"isLanded": false,
					"isScheduled": true,
					"sortTime": "2022-08-11T21:59:00.000Z"
				},
				"status": {
					"statusCode": "S",
					"status": "Scheduled",
					"color": "green",
					"statusDescription": "On time",
					"delay": {
						"departure": {
							"minutes": 0
						},
						"arrival": {
							"minutes": 0
						}
					},
					"delayStatus": {
						"wording": "On time",
						"minutes": 0
					},
					"lastUpdatedText": "Status Last Updated More Than 3 Hours Ago",
					"diverted": false
				},
				"resultHeader": {
					"statusDescription": "On time",
					"carrier": {
						"name": "United Airlines",
						"fs": "UA"
					},
					"flightNumber": "3867",
					"status": "Scheduled",
					"diverted": false,
					"color": "green",
					"departureAirportFS": "SCE",
					"arrivalAirportFS": "ORD",
					"divertedAirport": null
				},
				"ticketHeader": {
					"carrier": {
						"name": "United Airlines",
						"fs": "UA"
					},
					"flightNumber": "3867"
				},
				"operatedBy": "Operated by Air Wisconsin on behalf of United Airlines",
				"divertedAirport": null,
				"additionalFlightInfo": {
					"equipment": {
						"iata": "CR2",
						"name": "Canadair (Bombardier) Regional Jet 200",
						"title": "Actual"
					},
					"flightDuration": "1h 56m"
				},
				"codeshares": [],
				"positional": {
					"departureAirportCode": "SCE",
					"arrivalAirportCode": "ORD",
					"divertedAirportCode": null,
					"flexFlightStatus": "S",
					"flexTrack": {
						"flightId": 1104812458,
						"carrierFsCode": "ZW",
						"flightNumber": "3867",
						"tailNumber": "N465AW",
						"departureAirportFsCode": "SCE",
						"arrivalAirportFsCode": "ORD",
						"departureDate": {
							"dateUtc": "2022-08-11T21:59:00.000Z",
							"dateLocal": "2022-08-11T17:59:00.000"
						},
						"equipment": "CR2",
						"bearing": 281.7803912486057,
						"positions": [],
						"irregularOperations": [],
						"fleetAircraftId": 238160
					}
				},
				"flightState": "currentDatePreDeparture"
			},
			"route": {
				"header": {},
				"flights": [],
				"showCodeshares": null
			},
			"flightLoading": false
		}
	}
}
```

### Route Search

GET URL: https://www.flightstats.com/v2/flight-tracker/route/:departure/:arrival?year=:year&month=:month&date=:date&hour=:hour

Finds all routes going from a certain airport to another airport in a certain 6-hour period.

Parameters:
- departure: Must be an IATA 3 letter or an ICAO 4 letter airport code. For example: "SCE". Mandatory.
- arrival: Must be an IATA 3 letter or an ICAO 4 letter airport code. For example: "ORD". Mandatory.
- year: Year to lookup. Must be year with century. For example: "2022". Optional.
- month: Month to lookup. Can be zero-padded or not. For example: "2" or "02". Optional.
- date: Day to lookup. Can be zero-padded or not. For example: "3" or "03". Optional.
- hour: Hour to lookup. Must be either "0", "6", "12" or "18". Optional.

Example URL: https://www.flightstats.com/v2/flight-tracker/route/SCE/ORD/?year=2022&month=8&date=11&hour=6

Returns: [Extended Example.](/jsons/routesearch.json)
```
{
    "props": {
        "initialState": {
            "flightTracker": {
                "route": {
                    "header": {
                        "date": "11-Aug-2022",
                        "dateMDY": "Aug-11-2022",
                        "title": "(SCE) University Park Airport - (ORD) O'Hare International Airport",
                        "mobileTitle": "SCE - ORD Flights",
                        "departureAirport": {
                            "fs": "SCE",
                            "iata": "SCE",
                            "icao": "KUNV",
                            "name": "University Park Airport",
                            "city": "State College",
                            "state": "PA",
                            "country": "US",
                            "active": true,
                            "classification": 4,
                            "timeZoneRegionName": "America/New_York"
                        },
                        "arrivalAirport": {
                            "fs": "ORD",
                            "iata": "ORD",
                            "icao": "KORD",
                            "name": "O'Hare International Airport",
                            "city": "Chicago",
                            "state": "IL",
                            "country": "US",
                            "active": true,
                            "classification": 1,
                            "timeZoneRegionName": "America/Chicago"
                        }
                    },
                    "flights": [
                        {
                            "sortTime": "2022-08-11T11:00:00.000Z",
                            "departureTime": {
                                "timeAMPM": "7:00AM",
                                "time24": "07:00"
                            },
                            "arrivalTime": {
                                "timeAMPM": "8:01AM",
                                "time24": "08:01"
                            },
                            "carrier": {
                                "fs": "UA",
                                "name": "United Airlines",
                                "flightNumber": "3833"
                            },
                            "operatedBy": "Operated by Air Wisconsin on behalf of United Airlines",
                            "url": "/flight-tracker/UA/3833?year=2022&month=8&date=11&flightId=1104812497"
                        }
                    ],
                    "showCodeshares": null,
                    "destOriginTitle": null,
                    "carrierCode": ""
                }
            },
            "loading": {
                "LOAD_FLIGHT_TRACKER_ROUTE": false
            },
            "error": {
                "LOAD_FLIGHT_TRACKER_ROUTE": ""
            }
        }
    }
}
```

### Flight Tracker Map

GET URL: https://www.flightstats.com/v2/flight-tracker-map/:carrierCode/:number

Positional tracking for a flight on a map.

Parameters:
- carrierCode: Carrier (airline) IATA code. Mandatory.
- number: Flight number. Mandatory.

Example URL: https://www.flightstats.com/v2/flight-tracker-map/UA/3867

Returns: [Extended Example.](/jsons/flighttrackermap.json)
```
{
	"props": {
		"flightTracker": {
			"flight": {
				"flightId": 1104812458,
				"flightNote": {
					"final": false,
					"canceled": false,
					"hasDepartedGate": false,
					"hasDepartedRunway": false,
					"landed": false,
					"message": "Tracking will begin after departure",
					"messageCode": "S",
					"pastExpectedTakeOff": false,
					"tracking": false,
					"hasPositions": false,
					"trackingUnavailable": false,
					"phase": null,
					"hasActualRunwayDepartureTime": false,
					"hasActualGateDepartureTime": false
				},
				"isTracking": false,
				"isLanded": false,
				"isScheduled": true,
				"sortTime": "2022-08-11T21:59:00.000Z",
				"resultHeader": {
					"statusDescription": "On time",
					"carrier": {
						"name": "United Airlines",
						"fs": "UA"
					},
					"flightNumber": "3867",
					"status": "Scheduled",
					"diverted": false,
					"color": "green",
					"departureAirportFS": "SCE",
					"arrivalAirportFS": "ORD",
					"divertedAirport": null
				},
				"ticketHeader": {
					"carrier": {
						"name": "United Airlines",
						"fs": "UA"
					},
					"flightNumber": "3867"
				},
				"operatedBy": "Operated by Air Wisconsin on behalf of United Airlines",
				"divertedAirport": null,
				"additionalFlightInfo": {
					"equipment": {
						"iata": "CR2",
						"name": "Canadair (Bombardier) Regional Jet 200",
						"title": "Actual"
					},
					"flightDuration": "1h 56m"
				},
				"codeshares": [],
				"positional": {
					"departureAirportCode": "SCE",
					"arrivalAirportCode": "ORD",
					"divertedAirportCode": null,
					"flexFlightStatus": "S",
					"flexTrack": {
						"flightId": 1104812458,
						"carrierFsCode": "ZW",
						"flightNumber": "3867",
						"tailNumber": "N465AW",
						"departureAirportFsCode": "SCE",
						"arrivalAirportFsCode": "ORD",
						"departureDate": {
							"dateUtc": "2022-08-11T21:59:00.000Z",
							"dateLocal": "2022-08-11T17:59:00.000"
						},
						"equipment": "CR2",
						"bearing": 281.7803912486057,
						"positions": [],
						"irregularOperations": [],
						"fleetAircraftId": 238160
					}
				},
				"flightState": "currentDatePreDeparture"
			},
			"route": {
				"header": {},
				"flights": [],
				"showCodeshares": null
			},
			"flightLoading": false
		}
	}
}
```

### Flight Tracker Stops

GET URL: https://www.flightstats.com/v2/flight-tracker-stops/:carrierCode/:number

Get all the stops, or possible routes, for a flight.

Parameters:
- carrierCode: Carrier (airline) IATA code. Mandatory.
- number: Flight number. Mandatory.

Example URL: https://www.flightstats.com/v2/flight-tracker-stops/UA/3867

Returns: [Extended Example.](/jsons/flighttrackerstops.json)
```
{
    "props": {
        "isServer": true,
        "initialState": {
            "app": {
                "user": {},
                "appHost": "http://www.flightstats.com/v2"
            },
            "elasticSearch": {},
            "flick": {},
            "flightTracker": {
                "flight": {
                    "flightId": 1104962740,
                    "flightNote": {
                        "final": false,
                        "canceled": false,
                        "hasDepartedGate": false,
                        "hasDepartedRunway": false,
                        "landed": false,
                        "message": "Tracking will begin after departure",
                        "messageCode": "S",
                        "pastExpectedTakeOff": false,
                        "tracking": false,
                        "hasPositions": false,
                        "trackingUnavailable": false,
                        "phase": null,
                        "hasActualRunwayDepartureTime": false,
                        "hasActualGateDepartureTime": false
                    },
                    "isTracking": false,
                    "isLanded": false,
                    "isScheduled": true,
                    "sortTime": "2022-08-12T21:59:00.000Z",
                    "schedule": {
                        "scheduledDeparture": "2022-08-12T17:59:00.000",
                        "scheduledDepartureUTC": "2022-08-12T21:59:00.000Z",
                        "estimatedActualDepartureRunway": false,
                        "estimatedActualDepartureTitle": "Estimated",
                        "estimatedActualDeparture": "2022-08-12T17:59:00.000",
                        "estimatedActualDepartureUTC": "2022-08-12T21:59:00.000Z",
                        "scheduledArrival": "2022-08-12T18:55:00.000",
                        "scheduledArrivalUTC": "2022-08-12T23:55:00.000Z",
                        "estimatedActualArrivalRunway": false,
                        "estimatedActualArrivalTitle": "Estimated",
                        "estimatedActualArrival": "2022-08-12T18:55:00.000",
                        "estimatedActualArrivalUTC": "2022-08-12T23:55:00.000Z",
                        "graphXAxis": {
                            "dep": "2022-08-12T17:59:00.000",
                            "depUTC": "2022-08-12T21:59:00.000Z",
                            "arr": "2022-08-12T18:55:00.000",
                            "arrUTC": "2022-08-12T23:55:00.000Z"
                        }
                    },
                    "status": {
                        "statusCode": "S",
                        "status": "Scheduled",
                        "color": "green",
                        "statusDescription": "On time",
                        "delay": {
                            "departure": {
                                "minutes": 0
                            },
                            "arrival": {
                                "minutes": 0
                            }
                        },
                        "delayStatus": {
                            "wording": "On time",
                            "minutes": 0
                        },
                        "lastUpdatedText": "Status Last Updated 53 Minutes Ago",
                        "diverted": false
                    },
                    "resultHeader": {
                        "statusDescription": "On time",
                        "carrier": {
                            "name": "United Airlines",
                            "fs": "UA"
                        },
                        "flightNumber": "3867",
                        "status": "Scheduled",
                        "diverted": false,
                        "color": "green",
                        "departureAirportFS": "SCE",
                        "arrivalAirportFS": "ORD",
                        "divertedAirport": null
                    },
                    "ticketHeader": {
                        "carrier": {
                            "name": "United Airlines",
                            "fs": "UA"
                        },
                        "flightNumber": "3867"
                    },
                    "operatedBy": "Operated by Air Wisconsin on behalf of United Airlines",
                    "departureAirport": {
                        "fs": "SCE",
                        "iata": "SCE",
                        "name": "University Park Airport",
                        "city": "State College",
                        "state": "PA",
                        "country": "US",
                        "timeZoneRegionName": "America/New_York",
                        "regionName": "North America",
                        "gate": null,
                        "terminal": null,
                        "times": {
                            "scheduled": {
                                "time": "5:59",
                                "ampm": "PM",
                                "time24": "17:59",
                                "timezone": "EDT"
                            },
                            "estimatedActual": {
                                "title": "Estimated",
                                "time": "5:59",
                                "ampm": "PM",
                                "time24": "17:59",
                                "runway": false,
                                "timezone": "EDT"
                            }
                        },
                        "date": "2022-08-12T17:59:00.000"
                    },
                    "arrivalAirport": {
                        "fs": "ORD",
                        "iata": "ORD",
                        "name": "O'Hare International Airport",
                        "city": "Chicago",
                        "state": "IL",
                        "country": "US",
                        "timeZoneRegionName": "America/Chicago",
                        "regionName": "North America",
                        "gate": "F4",
                        "terminal": "2",
                        "baggage": null,
                        "times": {
                            "scheduled": {
                                "time": "6:55",
                                "ampm": "PM",
                                "time24": "18:55",
                                "timezone": "CDT"
                            },
                            "estimatedActual": {
                                "title": "Estimated",
                                "time": "6:55",
                                "ampm": "PM",
                                "time24": "18:55",
                                "runway": false,
                                "timezone": "CDT"
                            }
                        },
                        "date": "2022-08-12T18:55:00.000"
                    },
                    "divertedAirport": null,
                    "additionalFlightInfo": {
                        "equipment": {
                            "iata": "CR2",
                            "name": "Canadair (Bombardier) Regional Jet 200",
                            "title": "Actual"
                        },
                        "flightDuration": "1h 56m"
                    },
                    "codeshares": [],
                    "positional": {
                        "departureAirportCode": "SCE",
                        "arrivalAirportCode": "ORD",
                        "divertedAirportCode": null,
                        "flexFlightStatus": "S",
                        "flexTrack": {
                            "flightId": 1104962740,
                            "carrierFsCode": "ZW",
                            "flightNumber": "3867",
                            "tailNumber": "N415AW",
                            "departureAirportFsCode": "SCE",
                            "arrivalAirportFsCode": "ORD",
                            "departureDate": {
                                "dateUtc": "2022-08-12T21:59:00.000Z",
                                "dateLocal": "2022-08-12T17:59:00.000"
                            },
                            "equipment": "CR2",
                            "bearing": 281.7803912486057,
                            "positions": [],
                            "irregularOperations": [],
                            "fleetAircraftId": 63791
                        }
                    },
                    "flightState": "currentDatePreDeparture"
                },
                "route": {
                    "header": {},
                    "flights": [],
                    "showCodeshares": null
                },
                "flightLoading": false,
                "otherDays": [
                    {
                        "date1": "09-Aug",
                        "date2": "Aug-09",
                        "day": "Tuesday",
                        "year": "2022",
                        "flights": [
                            {
                                "arrivalAirport": {
                                    "city": "Chicago",
                                    "fs": "ORD",
                                    "iata": "ORD",
                                    "name": "O'Hare International Airport",
                                    "state": "IL",
                                    "country": "US"
                                },
                                "arrivalTime": "6:55",
                                "arrivalTimeAmPm": "PM",
                                "arrivalTime24": "18:55",
                                "arrivalTimezone": "CDT",
                                "departureAirport": {
                                    "city": "State College",
                                    "fs": "SCE",
                                    "iata": "SCE",
                                    "name": "University Park Airport",
                                    "state": "PA",
                                    "country": "US"
                                },
                                "departureTime": "5:59",
                                "departureTimeAmPm": "PM",
                                "departureTime24": "17:59",
                                "departureTimezone": "EDT",
                                "url": "/flight-tracker/UA/3867?year=2022&month=08&date=09&flightId=1104516048",
                                "sortTime": "2022-08-09T21:59:00.000Z"
                            }
                        ]
                    },
                    {
                        "date1": "10-Aug",
                        "date2": "Aug-10",
                        "day": "Wednesday",
                        "year": "2022",
                        "flights": [
                            {
                                "arrivalAirport": {
                                    "city": "Chicago",
                                    "fs": "ORD",
                                    "iata": "ORD",
                                    "name": "O'Hare International Airport",
                                    "state": "IL",
                                    "country": "US"
                                },
                                "arrivalTime": "6:55",
                                "arrivalTimeAmPm": "PM",
                                "arrivalTime24": "18:55",
                                "arrivalTimezone": "CDT",
                                "departureAirport": {
                                    "city": "State College",
                                    "fs": "SCE",
                                    "iata": "SCE",
                                    "name": "University Park Airport",
                                    "state": "PA",
                                    "country": "US"
                                },
                                "departureTime": "5:59",
                                "departureTimeAmPm": "PM",
                                "departureTime24": "17:59",
                                "departureTimezone": "EDT",
                                "url": "/flight-tracker/UA/3867?year=2022&month=08&date=10&flightId=1104664029",
                                "sortTime": "2022-08-10T21:59:00.000Z"
                            }
                        ]
                    },
                    {
                        "date1": "11-Aug",
                        "date2": "Aug-11",
                        "day": "Thursday",
                        "year": "2022",
                        "flights": [
                            {
                                "arrivalAirport": {
                                    "city": "Chicago",
                                    "fs": "ORD",
                                    "iata": "ORD",
                                    "name": "O'Hare International Airport",
                                    "state": "IL",
                                    "country": "US"
                                },
                                "arrivalTime": "6:55",
                                "arrivalTimeAmPm": "PM",
                                "arrivalTime24": "18:55",
                                "arrivalTimezone": "CDT",
                                "departureAirport": {
                                    "city": "State College",
                                    "fs": "SCE",
                                    "iata": "SCE",
                                    "name": "University Park Airport",
                                    "state": "PA",
                                    "country": "US"
                                },
                                "departureTime": "5:59",
                                "departureTimeAmPm": "PM",
                                "departureTime24": "17:59",
                                "departureTimezone": "EDT",
                                "url": "/flight-tracker/UA/3867?year=2022&month=08&date=11&flightId=1104812458",
                                "sortTime": "2022-08-11T21:59:00.000Z"
                            }
                        ]
                    },
                    {
                        "date1": "12-Aug",
                        "date2": "Aug-12",
                        "day": "Friday",
                        "year": "2022",
                        "flights": [
                            {
                                "arrivalAirport": {
                                    "city": "Chicago",
                                    "fs": "ORD",
                                    "iata": "ORD",
                                    "name": "O'Hare International Airport",
                                    "state": "IL",
                                    "country": "US"
                                },
                                "arrivalTime": "6:55",
                                "arrivalTimeAmPm": "PM",
                                "arrivalTime24": "18:55",
                                "arrivalTimezone": "CDT",
                                "departureAirport": {
                                    "city": "State College",
                                    "fs": "SCE",
                                    "iata": "SCE",
                                    "name": "University Park Airport",
                                    "state": "PA",
                                    "country": "US"
                                },
                                "departureTime": "5:59",
                                "departureTimeAmPm": "PM",
                                "departureTime24": "17:59",
                                "departureTimezone": "EDT",
                                "url": "/flight-tracker/UA/3867?year=2022&month=08&date=12&flightId=1104962740",
                                "sortTime": "2022-08-12T21:59:00.000Z"
                            }
                        ]
                    },
                    {
                        "date1": "13-Aug",
                        "date2": "Aug-13",
                        "day": "Saturday",
                        "year": "2022",
                        "flights": [
                            {
                                "arrivalAirport": {
                                    "city": "Chicago",
                                    "fs": "ORD",
                                    "iata": "ORD",
                                    "name": "O'Hare International Airport",
                                    "state": "IL",
                                    "country": "US"
                                },
                                "arrivalTime": "6:55",
                                "arrivalTimeAmPm": "PM",
                                "arrivalTime24": "18:55",
                                "arrivalTimezone": "CDT",
                                "departureAirport": {
                                    "city": "State College",
                                    "fs": "SCE",
                                    "iata": "SCE",
                                    "name": "University Park Airport",
                                    "state": "PA",
                                    "country": "US"
                                },
                                "departureTime": "5:59",
                                "departureTimeAmPm": "PM",
                                "departureTime24": "17:59",
                                "departureTimezone": "EDT",
                                "url": "/flight-tracker/UA/3867?year=2022&month=08&date=13&flightId=1105111128",
                                "sortTime": "2022-08-13T21:59:00.000Z"
                            }
                        ]
                    },
                    {
                        "date1": "14-Aug",
                        "date2": "Aug-14",
                        "day": "Sunday",
                        "year": "2022",
                        "flights": [
                            {
                                "arrivalAirport": {
                                    "city": "Chicago",
                                    "fs": "ORD",
                                    "iata": "ORD",
                                    "name": "O'Hare International Airport",
                                    "state": "IL",
                                    "country": "US"
                                },
                                "arrivalTime": "6:55",
                                "arrivalTimeAmPm": "PM",
                                "arrivalTime24": "18:55",
                                "arrivalTimezone": "CDT",
                                "departureAirport": {
                                    "city": "State College",
                                    "fs": "SCE",
                                    "iata": "SCE",
                                    "name": "University Park Airport",
                                    "state": "PA",
                                    "country": "US"
                                },
                                "departureTime": "5:59",
                                "departureTimeAmPm": "PM",
                                "departureTime24": "17:59",
                                "departureTimezone": "EDT",
                                "url": "/flight-tracker/UA/3867?year=2022&month=08&date=14&flightId=1105261276",
                                "sortTime": "2022-08-14T21:59:00.000Z"
                            }
                        ]
                    },
                    {
                        "date1": "15-Aug",
                        "date2": "Aug-15",
                        "day": "Monday",
                        "year": "2022",
                        "flights": []
                    }
                ]
            },
            "loading": {
                "LOAD_FLIGHT_TRACKER_FLIGHT": false,
                "LOAD_FLIGHT_TRACKER_OTHER_DAYS": false
            },
            "error": {
                "LOAD_FLIGHT_TRACKER_FLIGHT": "",
                "LOAD_FLIGHT_TRACKER_OTHER_DAYS": ""
            }
        },
        "initialProps": {
            "user": {},
            "pageProps": {
                "params": {
                    "carrierCode": "UA",
                    "flightNumber": "3867"
                },
                "isHistoricalFlight": false,
                "isOutOfDateRange": false,
                "head": {
                    "title": "UA3867 - United Airlines UA 3867 Flight Tracker",
                    "description": "UA3867 Flight Tracker - Track the real-time flight status of United Airlines UA 3867 live using the FlightStats Global Flight Tracker. See if your flight has been delayed or cancelled and track the live position on a map.",
                    "keywords": "United Airlines 3867 flight tracker, United Airlines 3867 flight status, UA 3867 flight tracker, UA 3867 flight status, United Airlines UA 3867 map, UA 3867, UA3867, United Airlines 3867",
                    "canonical": "/flight-tracker/UA/3867",
                    "noIndex": true
                },
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                "hostname": "www.flightstats.com"
            }
        }
    },
    "page": "/flight-tracker-stops",
    "pathname": "/flight-tracker-stops",
    "query": {
        "carrierCode": "UA",
        "flightNumber": "3867"
    },
    "buildId": "a8f0bc35-e41a-41f5-a4ba-f630d0aaa891",
    "assetPrefix": "https://assets.flightstats.com",
    "nextExport": false,
    "err": null,
    "chunks": []
}
```