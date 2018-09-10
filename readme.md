# mPulse Query API Wrapper

The python scripts are wrapper for [mPulse Query API](https://developer.akamai.com/api/web_performance/mpulse_query/v2.html). 

## Usage
To use the command, simply invoke the `akamai-mpulse` command with the right set of options. 

```
usage: akamai-mpulse [-h] [--config CONFIG] [--section SECTION] --api_key
                     API_KEY [--timer TIMER]
                     ...

CLI for mPulse Query API. For more information about the API, please refer to
https://developer.akamai.com/api/web_performance/mpulse_query/v2.html

positional arguments:
  args

optional arguments:
  -h, --help         show this help message and exit
  --config CONFIG    mPulse configuration file containing the user's API key
                     (deault=~/.mpulse)
  --section SECTION  Section within the config file containing the credentials
                     (default=[mpulse])
  --api_key API_KEY  API key of the app
  --timer TIMER      The timer to report (default=page load time)
```

The only _required_ parameter is the API key. 

By default, the function will use the following defaults:

- configuration file: `~/.mpulse`
- default section within this configuration file: `mpulse`
- under this configuration, it will look for 1 required and 1 optional parameter:
	- *apiToken*: This is the value pulled from the user's profile on the mPulse screen. This is a _required_ parameter.
	- *tenant*: Parameter used to restrict the security token to specific customer tenant.

![API token](token.png)	

## Optional Parameters
Apart from the parameters listed, any other parameter listed on the API page can be used. Here are a few examples:

- `timer`: (default _PageLoad_) This can be used to change the timer used for reported.
- `timezone`: (default _UTC_) Use this to change the _timezone_
- `type`: (default _summary_) This option switches the report. Possible options are :
	- summary
	- histogram
	- sessions-per-page-load-time
	- metric-per-page-load-time
	- by-minute
	- geography
	- page-groups
	- browsers
	- bandwidth
	- ab-tests
	- timers-metrics (for Navigation Timing, Custom Timers, and Custom Metrics)
	- metrics-by-dimension
	- dimension-values	