import groovy.json.JsonSlurper
import com.stackstate.stackpack.ProvisioningScript
import com.stackstate.stackpack.ProvisioningContext
import com.stackstate.stackpack.ProvisioningIO
import com.stackstate.stackpack.Version

class MuleSoftProvision extends ProvisioningScript {
  MuleSoftProvision(ProvisioningContext context) {
    super(context)
  }

  @Override
  ProvisioningIO<scala.Unit> install(Map<String, Object> config) {
    def cleanConfig = cleanupConfig(config)

    def templateArguments = [
      'topicName': topicName(cleanConfig),
      'integrationType': integrationType(cleanConfig),
      'organizationId': organizationId(cleanConfig),
      'instanceId': context().instance().id()
    ]
    templateArguments.putAll(cleanConfig)

    return context().stackPack().importSnapshot("templates/mulesoft-shared-template.stj", [:]) >>
           context().instance().importSnapshot("templates/mulesoft-instance-template.stj", templateArguments)
  }

  @Override
  ProvisioningIO<scala.Unit> upgrade(Map<String, Object> config, Version current) {
    return install(config)
  }

  @Override
  void waitingForData(Map<String, Object> config) {
    context().sts().onDataReceived(topicName(config), {
      context().sts().provisioningComplete()
    })
  }

  private def cleanupConfig(Map<String, Object> config) {
    def cleanConfig = [:]
    cleanConfig.putAll(config)
    cleanConfig.organization_id = config.organization_id.trim()

    return cleanConfig
  }

  private def topicName(Map<String, Object> config) {
    def url = config.organization_id
    def type = integrationType()
    return context().sts().createTopologyTopicName(type, url)
  }

  private def integrationType(Map<String, Object> config) {
    return 'mulesoft'
  }

  private def organizationId(Map<String, Object> config) {
    return config.organization_id
  }
}
