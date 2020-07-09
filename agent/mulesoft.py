import logging
import time
import requests
from stackstate_checks.base import ConfigurationError, AgentCheck, TopologyInstance


class MuleSoftCheck(AgentCheck):
    INSTANCE_TYPE = "mulesoft"
    SERVICE_CHECK_NAME = "mulesoft.can_connect"

    def __init__(self, name, init_config, instances=None):
        AgentCheck.__init__(self, name, init_config, instances)
        self.session = requests.Session()
        self.organization_id = None

    def get_instance_key(self, instance):
        if "organization_id" not in instance:
            raise ConfigurationError("Missing 'organization' in instance configuration.")
        return TopologyInstance(self.INSTANCE_TYPE, str(self.organization_id))

    def check(self, instance):
        username = instance.get("username",  "") 
        password = instance.get("password", "")
        self.organization_id = instance.get("organization_id", None)
        tags = instance.get("tags", [])

        if not (username and password):
            raise ConfigurationError("Missing 'username' or 'password' in instance configuration.")

        try:
            self.start_snapshot()

            #self._authenticate(username, password)

            self._collect_topology()

            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, message="OK", tags=["organization_id:%s" % self.organization_id])
        except Exception as e:
            self.log.exception(str(e))
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, message=str(e), tags=["organization_id:%s" % self.organization_id])
        finally:
            self.stop_snapshot()

    def _authenticate(self, user, password):
        url = 'https://anypoint.mulesoft.com/accounts/login'
        data = """{
          "username": "testUser",
          "password": "Password1"
        }
        """
        #resp = self.session.post(url, data=data)
        #print(resp)
        url = 'https://anypoint.mulesoft.com/accounts/login'
        body = """{
          "username": "%s",
          "password": "%s"
        }
        """ % (user, password)

        resp = self.session.post(url, data=body)
        resp.raise_for_status()
        
        print(resp.status_code)
        print(resp.headers)
        print(resp.text)

        bearer_token = resp.json().get("access_token", None)
        raise CheckError("Did not receive a brearer token from MuleSoft, got: %s." % resp.text)

        self.session.headers.update({'Authentication': "bearer %s" % bearer_token})

    def _collect_topology(self):
        self.component(id="myapi", type="api", data={
            "organization_id": self.organization_id
            })
        

