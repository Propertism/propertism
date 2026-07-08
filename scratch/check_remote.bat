eb ssh -c "sudo tee /tmp/check_prod.sh << 'EOF'
#!/bin/bash
export \$(sudo cat /opt/elasticbeanstalk/deployment/env | xargs)
/var/app/venv/staging-LQM1lest/bin/python /var/app/current/manage.py shell -c 'from chat.models import BusinessRule, ServiceProfile, KnowledgeArticle, KnowledgeDocument, ConfigurationItem; print(\"BusinessRule:\", BusinessRule.objects.count()); print(\"ServiceProfile:\", ServiceProfile.objects.count()); print(\"KnowledgeArticle:\", KnowledgeArticle.objects.count()); print(\"KnowledgeDocument:\", KnowledgeDocument.objects.count()); print(\"ConfigurationItem:\", ConfigurationItem.objects.count())'
EOF
sudo chmod +x /tmp/check_prod.sh
sudo /tmp/check_prod.sh"
