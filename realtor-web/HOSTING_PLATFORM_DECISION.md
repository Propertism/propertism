# Hosting Platform Decision Document

**Project**: Propertism Realty Advisors LLP  
**Date**: February 25, 2026  
**SCCB**: SCCB-47 Compliance  
**Status**: Decision Required

---

## Purpose

This document helps you choose the right hosting platform for production deployment.

---

## Comparison Matrix

| Feature | Ubuntu VPS | Render | Railway | DigitalOcean App |
|---------|-----------|--------|---------|------------------|
| **Cost/Month** | $12-20 | $7-25 | $5-20 | $12-25 |
| **Setup Complexity** | High | Low | Low | Medium |
| **SSL** | Manual (Certbot) | Automatic | Automatic | Automatic |
| **Database** | Self-managed | Managed | Managed | Managed |
| **Scaling** | Manual | Automatic | Automatic | Automatic |
| **Control** | Full | Limited | Limited | Medium |
| **Deployment** | Git + SSH | Git push | Git push | Git push |
| **Monitoring** | Self-setup | Built-in | Built-in | Built-in |
| **Backups** | Manual | Automatic | Automatic | Automatic |

---

## Option 1: Ubuntu VPS (Recommended for Full Control)

### Pros
✅ Full server control  
✅ Cost-effective for long-term  
✅ Can host multiple projects  
✅ Complete customization  
✅ No vendor lock-in  

### Cons
❌ Requires server management skills  
❌ Manual SSL setup  
❌ Manual backups  
❌ Security is your responsibility  
❌ More time to set up  

### Best For
- Developers comfortable with Linux
- Long-term projects
- Multiple applications
- Custom requirements

### Providers
- **DigitalOcean**: $12/month (2GB RAM, 50GB SSD)
- **Linode**: $12/month (2GB RAM, 50GB SSD)
- **Vultr**: $12/month (2GB RAM, 55GB SSD)
- **AWS EC2**: t3.small (~$15/month)

### Setup Time
4-6 hours (first time)  
1-2 hours (with experience)

---

## Option 2: Render (Recommended for Simplicity)

### Pros
✅ Zero-config deployment  
✅ Automatic SSL  
✅ Managed PostgreSQL  
✅ Auto-scaling  
✅ Built-in monitoring  
✅ Automatic backups  
✅ Free tier available  

### Cons
❌ Less control  
❌ Vendor lock-in  
❌ Can be expensive at scale  

### Best For
- Quick deployment
- First-time deployers
- Focus on development, not DevOps
- Startups

### Pricing
- **Starter**: $7/month (512MB RAM)
- **Standard**: $25/month (2GB RAM)
- **PostgreSQL**: $7/month (1GB storage)

### Setup Time
30 minutes

### Deployment Steps
1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

---

## Option 3: Railway

### Pros
✅ Extremely simple deployment  
✅ Automatic SSL  
✅ Built-in PostgreSQL  
✅ $5 free credit/month  
✅ Pay-as-you-go  

### Cons
❌ Can be expensive with traffic  
❌ Less mature than competitors  

### Best For
- Hobby projects
- MVPs
- Testing production setup

### Pricing
- $5 free credit/month
- $0.000463/GB-hour RAM
- $0.25/GB storage

### Setup Time
15 minutes

---

## Option 4: DigitalOcean App Platform

### Pros
✅ Managed deployment  
✅ Automatic SSL  
✅ Good documentation  
✅ Integrated with DO ecosystem  
✅ Auto-scaling  

### Cons
❌ More expensive than VPS  
❌ Less flexible than raw VPS  

### Best For
- DigitalOcean users
- Medium-sized projects
- Teams

### Pricing
- **Basic**: $12/month (512MB RAM)
- **Professional**: $25/month (1GB RAM)
- **Database**: $15/month

### Setup Time
1 hour

---

## Decision Framework

### Choose Ubuntu VPS if:
- [ ] You have Linux/DevOps experience
- [ ] You want full control
- [ ] You plan to host multiple projects
- [ ] You want lowest long-term cost
- [ ] You're comfortable with server management

### Choose Render if:
- [ ] You want fastest deployment
- [ ] You're new to deployment
- [ ] You want managed services
- [ ] You prefer automatic backups
- [ ] You want to focus on development

### Choose Railway if:
- [ ] You're testing/prototyping
- [ ] You want lowest initial cost
- [ ] You have low traffic expectations
- [ ] You want simplest setup

### Choose DigitalOcean App Platform if:
- [ ] You already use DigitalOcean
- [ ] You want managed but flexible
- [ ] You need good documentation
- [ ] You have medium budget

---

## Recommended Decision Path

### For Initial Launch (Recommended)
**Use Render or Railway**
- Get to market fast
- Automatic SSL and backups
- Focus on product, not infrastructure
- Migrate to VPS later if needed

### For Long-Term (6+ months)
**Use Ubuntu VPS**
- Lower cost at scale
- Full control
- Better performance
- More flexibility

---

## Traffic Estimates

### Low Traffic (< 1,000 visitors/day)
- **Render Starter**: $7/month ✅
- **Railway**: $5-10/month ✅
- **Ubuntu VPS**: $12/month ✅

### Medium Traffic (1,000-10,000 visitors/day)
- **Render Standard**: $25/month
- **Railway**: $15-30/month
- **Ubuntu VPS**: $12-20/month ✅ (best value)

### High Traffic (10,000+ visitors/day)
- **Ubuntu VPS**: $20-50/month ✅
- **Render**: $50-100/month
- Consider CDN + Load Balancer

---

## Final Recommendation

### Phase 1: Launch (Months 1-3)
**Platform**: Render  
**Cost**: ~$14/month (app + database)  
**Reason**: Fast deployment, automatic SSL, managed services

### Phase 2: Growth (Months 4-12)
**Platform**: Ubuntu VPS (DigitalOcean)  
**Cost**: ~$12/month  
**Reason**: Better cost/performance, full control

### Migration Path
1. Launch on Render
2. Validate product-market fit
3. Migrate to VPS when traffic grows
4. Use Render deployment guide as reference

---

## Decision Record

**Date**: _________________  
**Platform Chosen**: _________________  
**Reason**: _________________  
**Expected Cost**: _________________  
**Deployment Date**: _________________

---

## Next Steps

Once platform is chosen:

1. [ ] Create account on chosen platform
2. [ ] Set up database
3. [ ] Configure environment variables
4. [ ] Deploy application
5. [ ] Configure domain
6. [ ] Set up SSL
7. [ ] Test thoroughly
8. [ ] Update this document with actual deployment details

---

**Document Owner**: Viji  
**Last Updated**: February 25, 2026  
**SCCB Compliance**: SCCB-47 ✅
