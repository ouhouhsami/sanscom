# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.conf import settings
import ads.models.search
import django_extensions.db.fields


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# ads.migrations.0004_auto_20150312_1420
# ads.migrations.0002_auto_20150304_0915

a_propos = '''
<h3>Achetersanscom c’est :</h3>
<ul>
<li>gratuit pour les acheteurs et les vendeurs</li>
<li>sans intermédiaire et sans commission sur les ventes</li>
<li>la définition de sa propre zone de recherche en dessinant directement sur une carte</li>
<li>des annonces détaillées et complètes évitant les visites et appels inutiles</li>
</ul>
<p>
Achetersanscom est un site d’annonces immobilières entièrement gratuit, sans aucune publicité et sans intermédiaire, qui permet une recherche personnalisée des biens en vente en dessinant sa propre zone de recherche sur une carte.
</p>
<p>
Les annonces sont géolocalisées et permettent d’avoir depuis chez soi toutes les informations indispensables sur les biens à vendre: cela évite les coups de fil et les visites inutiles, que ce soit pour les acheteurs ou les vendeurs.
</p>
<p>
Le but de ce site est de faciliter la mise en vente et la recherche de biens immobiliers en évitant de payer des commissions qui peuvent aller jusqu’à 10% du prix de vente dans un marché déjà excessif et pour des services qui ne répondent pas toujours à vos attentes et vos objectifs.
</p>

<h3>Qui sommes nous ?</h3>

<p>
Primo-accédants, nous avons mis plusieurs années avant de trouver le bien qui nous convenait, dans nos prix et dans le quartier que l’on souhaitait.
<br>
Nous avons passé des centaines d’appels pour des annonces systématiquement incomplètes, voire trompeuses, visité des dizaines de biens, lorsque le RDV n’a pas été annulé 5 minutes avant voire lorsque personne n’est present au RDV, apprécié la plue-value d’intermediaires passant le seuil de la porte en même temps que nous pour la première fois, incapable de donner des informations techniques autres que celles figurant dans l’annonce.
</p>
<p>
Le manque d’information notamment sur la localisation des biens nous obligeant systématiquement à contacter les vendeurs ou les intermediaires pour avoir des informations que nous aurions pu avoir directement sur le site, évitant ainsi de perdre du temps, pour nous, le vendeur et les agences immobilières. Quand les annonces immobilières ne proposent pas de recherche localisée géographiquement, celle-ci prédéfinit des zones qui ne correspondent pas aux choix de l’acheteur ou la localisation du bien reste trop vague pour apprécier la situation exacte de la rue.
</p>
<p>
Après avoir finalement acheté un bien, via une agence et payé plusieurs dizaine de milliers d’euros pour un service inexistant, nous avons decidé de créer un service utile proposant des annonces immoibilieres, sans interméidaire et qui aurait pu correspondre à nos besoins lors de nos recherches.
</p>

<h3>Pourquoi utiliser Achetersanscom.com ?</h3>

<h4>Vous êtes acheteur :</h4>
<p>
Vous pouvez définir votre zone idéale de recherche en dessinant sur une carte et trouver les biens en vente dans cette zone.
Les formulaires de mise en vente des biens guident les vendeurs afin que ceux-ci renseignent tous les critères necessaires pour caractériser de la manière la plus exhaustive et la plus complète possible leur logement. Cela vous permet de faire une première sélection des biens et vous évite les contacts par téléphone ou les visites inutiles.
<br>
La recherche est gratuite et le site fontionne sans publicité.
<br>
Vous pouvez enregistrer vos recherches et créer des alertes email, pour être tenu informé de la publication de nouveaux biens correspondant à vos critères.
</p>

<h4>Vous êtes vendeur :</h4>
<p>
La mise en vente de votre bien est entièrement gratuite. Nos formulaires de mise en vente des biens vous guident pas à pas dans la rédaction de votre annonce, vous aidant ainsi à mettre en valeur votre bien et à n’oublier aucun renseignement sur votre bien.
<br>
Les acheteurs potentiels bénéficient d’une recherche géolocalisées à partir d’une zone qu’ils peuvent définir eux-mêmes sur une carte et peuvent ainsi cibler de manière efficace les annonces qui les intéressent. Seuls les acheteurs véritablement intéréssés par votre bien vous contacte, ce qui vous évite de répondre à de nombreux appels et d’organiser des visites qui n’auront pas de suite.
<br>
En mettant votre bien en vente sur Achetersanscom, vous optimisez la réussite de vente de votre bien et ne perdez pas de temps, le tout sans aucun frais.
</p>


<h3>Comment le site est financé ?</h3>

<p>
Nous avons concu ce site sans aucune publicité. La mise en ligne des annonces et leur consultation est entièrement gratuite. Nous sommes bénévoles et absolument pas rémunérés par le site.
<br>
Nous financons l’hébergement du site sur nos propres fonds.
</p>
'''

cgu = '''
<h3>0. Acceptation et modifications des CGU :</h3>

<p>
L'accès, la consultation, l’utilisation ou la souscription aux Services sont gratuits mais restent subordonnés à l'acceptation sans reserve ni restrictions des CGU.
<br>
Les CGU applicables sont celles en vigueur et accessibles sur Achetersanscom à la date d'accès au site par l'Utilisateur.
<br>
Achetersanscom se réserve le droit de modifier les CGU, librement et à tout moment,.
Chaque Utilisateur est invité à consulter régulièrement les CGU afin de prendre connaissance de changements éventuels.
</p>

<h3>1. Définitions :</h3>

<p>
Au sens des présentes conditions générales d’utilisation, on entend par :
</p>
<p>
“Achetersanscom” : le service électronique interactif accessible notamment à l’adresse http://www.achetersanscom.com
<br>
“CGU” : les présentes conditions générales d’utilisation d’Achetersanscom
<br>
“Compte”: l’espace personnel que peut créer l’Utilisateur et qui offre les Services décrits au point 2.2 des CGU
<br>
“Services” : l’ensemble des possibilités offertes à l’Utilisateur sur Achetersanscom et décrites au point 2 des CGU
<br>
“Utilisateur” : toute personne qui accède à achetersanscom et utilise les Services
</p>

<h3>2. Services fournis :</h3>

<h4>2.1. Objet :</h4>

<p>
Achetersanscom est un site internet de mise en ligne et de recherche d’annonces immobilières géolocalisées, entre particuliers.
<br>
Achetersanscom n’est pas une agence immobilière, ni un professionnel de l’immobilier. Il n’y a donc aucun contrat à signer ni aucune commission à payer lors de la vente d’un bien, réalisée par l’intermédiaire d’Achetersanscom.
</p>

<p>
Les Services fournis consistent à faciliter les démarches de l'Utilisateur dans sa recherche d'achat ou de vente d'un bien immobilier en lui permettant de bénéficier des Services suivants :
</p>
<ul>
<li>recherche de biens immobiliers en vente par des particuliers et sans commission</li>
<li>recherche des offres à partir d’une zone géographique définie par l’Utilisateur sur une carte (recherche géolocalisée) et à partir de critères portant sur les biens</li>
<li>mise en ligne d’une annonce de vente de biens immobiliers sans commission</li>
<li>création d’un Compte au travers duquel l’Utilisateur peut enregistrer ses recherches et ses annonces</li>
<li>souscription à une alerte par courrier électronique pour recevoir les annonces correspondant aux critères de recherche définis par l’Utilisateur</li>
<li>accès aux coordonnées des vendeurs ayant mis en ligne des annonces de vente de biens immobiliers, sans frais</li>
<li>consultation des annonces de vente de biens immobiliers, sans frais </li>
<li>souscription à une alerte par courrier électronique pour recevoir les informations de mise à jour du Site Internet</li>
</ul>
<h4>2.2. Compte de l’Utilisateur:</h4>

<p>
La creation d’un Compte est rendu possible pour tout Utilisateur à partir de la page d’accueil, en se rendant sur la rubrique “s’inscrire”.
</p>
<p>
L’Utilisateur renseigne une adresse de courier électronique valide et choisit un mot de passe.
<br>
L’adresse de courier électronique constitue son identifiant et est unique.
<br>
Le mot de passé fournit est strictement personnel.
<br>
L'Utilisateur s'engage à conserver ces données confidentielles et à ne pas les transmettre à des tiers.
<br>
L'Utilisateur est seul autorisé à accéder et utiliser les Services à l'aide de son identifiant unique et de son mot de passe.
<br>
Tout accès au Compte de l'Utilisateur avec son identifiant et son mot de passe :
</p><ul>
<li>est réputé de plein droit avoir été effectué par l'Utilisateur</li>
<li>et s'effectue sous la seule responsabilité de l'Utilisateur</li>
</ul>
<p>
En cas de perte, de vol ou de tout acte frauduleux à l'égard de son identifiant et de son mot de passe, l'Utilisateur en informe Achetersanscom dans les plus brefs délais. Sous reserve de justifier de son identité par tous moyens, Achetersanscom adresse à l'Utilisateur un nouvel identifiant et un nouveau mot de passe.
</p>
<p>
L’Utilisateur peut renseigner son numéro de telephone, utile notamment pour être contacté par les autres Utilisateurs qui souhaitent des informations complémentaires sur son(ses) annonce(s) de vente le cas échéant.
</p>
<p>
L’Utilisateur peut modifier à tout moment ses informations personnels dans son Compte.
</p>

<h4>2.3. Mise en ligne d’une annonce de vente</h4>

<p>
La mise en ligne d'une annonce de vente sur achetersanscom.com implique pour l’Utilisateur, l'acceptation sans réserve des présentes CGU.
</p>
<p>
Achetersanscom se réserve le droit de retirer toute annonce ou tout contenu qui ne respecterait pas les présentes CGU sans avertissement ou notification. Un tel refus ne fait naître au profit de l’utilisateur aucun droit à indemnité.
</p>
<p>
L'annonce est diffusée sous la responsabilité exclusive de l’Utilisateur.
</p>
<p>
L’annonce ne devra pas comporter de texte qui sembleraient contraires aux dispositions légales ou réglementaires, aux bonnes mœurs, ou susceptible de troubler ou choquer les autres utilisateurs. Le texte de l’annonce doit décrire uniquement le bien en vente.
Les images publiées par l’Utilisateur dans son annonce ne doivent représenter que le bien en vente.
</p>
<p>
L’annonce ne devra concerner qu’un seul bien. En cas de vente de plusieurs biens, l’utilisateur devra créer une autre annonce. Si l’Utilisateur souhaite insérer une nouvelle annonce relative au meme bien, il devra au préalable supprimer l’annonce existante.
</p>
<p>
L’Utilisateur qui publie une annonce de vente de son bien sur Achetersanscom consent à ce que l’ensemble des informations qu’il renseigne dans son annonce soit publié sur Achetersanscom pendant toute la durée de validité de l’annonce.
</p>
<h4>2.4. Alerte Email :</h4>
<p>
Achetersanscom.com est susceptible d'adresser à l'Utilisateur, par courrier électronique ou par téléphone, des informations sur l’actualité du Site Internet, sauf refus émis par l’utilisateur.
</p>
<h4>2.5. Disponibilités des Services :</h4>
<p></p>
Les Services sont disponibles 24 heures sur 24 et 7 jours sur 7, sauf pour raisons de maintenance des Services et/ou des serveurs et/ou d’Achetersanscom.
<br>
Achetersanscom se réserve la possibilité de modifier, interrompre, à tout moment, temporairement ou de manière permanente tout ou partie des Services sans information préalable des Utilisateurs et sans droit à indemnités.
<p></p>

<h3>3. Garanties de l’Utilisateur :</h3>

<p>
Achetersanscom est strictement reservé aux Utilisateurs particuliers et ne peut en aucun cas être utilisé par les professionnels de l’immobilier ou tout autre intermédiaire, que ce soit pour deposer une annonce ou pour contacter un Utilisateur.
</p>
<p>
Si vous avez déposé une annonce sur Achetersanscom en tant qu’Utilisateur particulier et que vous avez été contacté par ce biais par un professionnel de l’immobilier ou tout autre intermédiaire, merci de nous le signaler en nous écrivant à contact@achetersanscom.com.
</p>

<p>
En outre, l'Utilisateur s'engage à :
</p>
<ul>
<li>utiliser Achetersanscom et ses Services en toute bonne foi ;</li>
<li>respecter les CGU ;</li>
<li>utiliser les Services de manière raisonnable et dans un but strictement privé et personnel ;</li>
<li>ne pas réutiliser, exploiter, commercialiser, extraire ou reproduire tout ou partie des Services ainsi que le contenu d’Achetersanscom, en particulier des annonces, que ce soit à des fins commerciales ou non, collectives ou personnelles, directement ou indirectement, quelque soit la forme, et quelque soit le media utilisé ;</li>
<li>ne pas affecter ou ne pas tenter d’affecter le bon fonctionnement des Services de quelque manière que ce soit ;</li>
<li>ne pas limiter out enter de limiter l’accès aux Services et leur utilization, de quelque manière que ce soit ;</li>
<li>ne pas accéder aux Services à des fins illicites ou dans le but de causer un préjudice à la réputation et l'image d’Achetersanscom ou plus généralement à porter atteinte aux droits, notamment de propriété intellectuelle d’achetersanscom ou de tiers ;</li>
<li>ne pas modifier le contenu d’Achetersanscom, hormis ses données personnelles figurant dans son Compte </li>
<li>ne pas contrevenir aux dispositions des articles 323-1 à 323-7 du Code Pénal réprimant les pratiques dites de " hacking " ;</li>
<li>ne pas utiliser ou exploiter les informations personnelles des autres Utilisateurs en vue de les contacter pour leur proposer des services dans un cadre professionnel, que la sollicitation soit individuelle ou en masse ;</li>
<li>ne pas récupérer ou d’indexer tout ou partie du contenu d’Achetersanscom, quelque soit le moyen utilisé ; </li>
<li>ne pas copier tout ou partied u contenu d’Achetersanscom sur des supports quelque soit leur nature permettant de reconstituer tout ou partie des fichiers d'origine ;</li>
<li>ne pas mettre en place de liens hypertextes à destination de pages profondes d’Achetersanscom, permettant l'accès aux Services en passant outré le champ d’identification de l’Utilisateur, et quelque soit le moyen utilisé </li>
<li>ne pas procéder à l'aspiration de tout ou partie du contenu d’Achetersanscom.
</li>
</ul>
<p>
En cas de manquement à l'une de ces obligations et, sans que cette liste ne soit limitative, l'Utilisateur reconnaît et accepte qu’Achetersanscom a la faculté de lui refuser, unilatéralement et sans notification préalable, l'accès aux Services.
</p>

<h3>4. Garanties et responsabilités d’Achetersanscom :</h3>

<p>
Achetersanscom met à la disposition de l'Utilisateur l’accès aux Services décrits au point 2 des CGU et ne peut garantir notamment :
</p>
<ul>
<li>de suites favorables aux demandes de mise en contact effectuées par l’Utilisateur auprès d’un autre Utilisateur ;</li>
<li>la disponibilité à tout moment des biens affichés sur Achetersanscom ;</li>
<li> la conclusion de relation contractuelle entre les Utilisateurs et notamment, la vente effective à l’Utilisateur d’un bien dont l’annonce figure sur Achetersanscom.</li>
</ul>
<p>
Achetersanscom décline toute responsabilité quant à la fiabilité, la pertinence ou la validité des informations fournies dans les annonces mises en ligne par les Utilisateurs. Ces informations sont de la responsabilité de l’Utilisateur conformément au point 3 des CGU.
</p>
<p>
En outre, Achetersanscom décline toute responsabilité:
</p>
<ul>
<li>en cas d'interruption des Services pour des opérations de maintenance, d’actualisation ou de mise à jour ;
</li>
<li>en cas d'indisponibilité des Services pour des raisons indépendantes de la volonté d’Achetersanscom ;
</li>
<li>en cas d'impossibilité momentanée d'accès aux Services en raison de problèmes techniques et ce quelles qu'en soient l'origine et la provenance,
</li>
<li> en cas de dommages directs ou indirects causés à l'Utilisateur, quelle qu'en soit la nature, résultant du contenu, de l'accès, ou de l'utilisation des Services ;
</li>
<li>en cas d'utilisation des Services par un Utilisateur dans des conditions non conformes aux CGU ;
</li>
<li>en cas d'utilisation anormale ou illicite des Services. L'utilisateur est alors seul responsable des dommages causés aux tiers et des conséquences des réclamations ou actions qui pourraient en découler. L'utilisateur renonce à exercer tout recours contre Achetersanscom dans le cas de poursuites diligentées par un tiers à son encontre du fait de l'utilisation illicite du site ;
</li>
<li>en cas de contenu de sites internet de tiers qui contreviendrait aux dispositions légales ou réglementaires en vigueur, accessibles depuis des liens hypertextes contenus sur Achetersanscom. La décision d'activer ces liens relève de la pleine et entière responsabilité de l’Utilisateur.
</li>
</ul>
<p>
Achetersanscom n’est tenu en aucun cas à reparation, de quelque nature que ce soit, du fait d'erreurs ou d'omissions dans le contenu d'une annonce, ou de défaut de parution de celle-ci.
</p>
<p>
Achetersanscom.com se réserve le droit de suspendre ou d'arrêter les Services sans être tenue de verser aux Utilisateurs une indemnité de quelque nature que ce soit.
</p>

<h3>5. Droit de propriété intellectuelle et responsabilités :</h3>

<p>
Achetersanscom est le titulaire des droits de propriété intellectuelle du site internet et de l’ensemble de son contenu (textes, graphismes, logiciels, slogans, graphiques, images, vidéos, sons, plans, logos, marques, bases de données, photos et autres contenus), hormis les elements realisés par des intervenants extérieurs n’ayant pas cede leurs droits d’auteur.
<br>
L'Utilisateur accepte que l'utilisation du site et des Services n’emporte quelconque cession ou concession de droits et notamment de droits d'auteurs.
</p>
<p>
Toute utilisation contraire aux dispositions des présentes CGU est susceptible d’entrainer une violation des droits d’auteurs, de constituer des actes de contrefaçon ou une atteinte au droit de divulgation d’achetersanscom et peut engager la responsabilité pénale et/ou civile de l'Utilisateur.
</p>

<h3>6. Droit applicable et réglements des litiges :</h3>

<p>
Les présentes CGU sont soumises au droit français.
Achetersanscom se réserve la possibilité de saisir toutes voies de droit à l'encontre des personnes qui n'auraient pas respecté les CGU.
En cas de litige relatif à l'application, l'interprétation, la validité, l’acceptation et l'exécution de ces conditions, et à défaut d'accord amiable entre les parties, les tribunaux de Paris seront seuls compétents.
</p>

<h3>Contact :</h3>

<p>
Pour toute information de nature technique ou relative au fonctionnement des Services, l'Utilisateur est invité à envoyer un courrier électronique à l’adresse suivante: contact@achetersanscom.com
</p>
<p>
Toute réclamation, pour être recevable, doit être transmise par courrier électronique à l’adresse suivante : contact@achetersanscom.com dans un délai de quarante huit (48) heures à compter de la date de diffusion sur Achetersanscom.
</p>
'''

legal = '''
<p>
Edition : Achetersanscom
<br>
Hébergement : Alwaysdata https://www.alwaysdata.com/
</p>

<p>
Déclaration CNIL (Commission Nationale Informatique et Liberté) : dossier n°1440427.
</p>
<p>
Vous disposez d'un droit d'accès, de modification, de rectification, et de suppression des données vous concernant conformément à la loi n°78-17 du 6 janvier 1978 modifiée par la loi n°2004-81 du 6 août 2004.
Pour exercer ce droit, contactez nous par email (contact@achetersanscom.com). Vous pouvez également et à tout moment, modifier les informations personnelles vous concernant à partir de votre espace personnel “mon compte”.
</p>
<p>
Les données recueillies lors de la creation de votre espace personnel “mon compte” et le cas échéant de la mise en ligne d’une annonce sont strictement confidentielles et ne sont pas transmises à des tiers, sauf réquisition judiciaire ou demande d'une autorité habilitée. Les champs à remplir obligatoirement sont signalés par une *.
</p>
<p>
Lorsque de la connexion à votre espace personnel “mon compte”, la trace des connexions électroniques sont conservées. L'ensemble des données à caractère personnel font l'objet d'un archivage électronique jusqu’à la suppresion de votre annonce ou votre désinscription.
</p>
<p>
Des cookies peuvent être utilisés afin par exemple de conserver les critères de recherche. Un cookie ne permet en aucun cas d’identifier l’Utilisateur et disparaît à chaque nettoyage des fichiers temporaires. L'Utilisateur a la faculté de s'opposer à l'enregistrement de ces cookies et ce notamment en configurant son navigateur Internet.
</p>
'''

flatpages = [
    {'url': '/a-propos/', 'title': 'A propos', 'content':a_propos},
    {'url': '/legal/', 'title': 'Conditions générales d\'utilisation', 'content':legal},
    {'url': '/cgu/', 'title': 'Mentions légales', 'content':cgu},
]

def fill_flatpages(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FlatPage = apps.get_model("flatpages", "FlatPage")
    Site = apps.get_model("sites", "Site")
    site = Site.objects.create(domain='achetersanscom.com', name='AcheterSansCom')
    for flatpage in flatpages:
        fp = FlatPage.objects.create(url=flatpage['url'], title=flatpage['title'], content=flatpage['content'])
        fp.sites.add(site)


def create_habitation_types(apps, schema_editor):
    HabitationType = apps.get_model("ads", "HabitationType")
    db_alias = schema_editor.connection.alias
    HabitationType.objects.using(db_alias).bulk_create([
        HabitationType(label="Appartement"),
        HabitationType(label="Maison")
    ])


class Migration(migrations.Migration):

    replaces = [(b'ads', '0001_initial'), (b'ads', '0002_auto_20150304_0915'), (b'ads', '0003_auto_20150305_1102'), (b'ads', '0004_auto_20150312_1420'), (b'ads', '0005_auto_20150312_1455'), (b'ads', '0006_search_rooms_min'), (b'ads', '0007_auto_20150317_1948'), (b'ads', '0008_auto_20150321_1158')]

    dependencies = [
        ('flatpages', '0001_initial'),
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'slug_format', verbose_name='slug', editable=False, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Localisation')),
                ('address', models.CharField(max_length=255, verbose_name='Adresse')),
                ('price', models.PositiveIntegerField(verbose_name='Prix')),
                ('surface', models.IntegerField(verbose_name='Surface habitable')),
                ('surface_carrez', models.IntegerField(null=True, verbose_name='Surface Loi Carrez', blank=True)),
                ('rooms', models.PositiveIntegerField(verbose_name='Nombre de pi\xe8ces')),
                ('bedrooms', models.PositiveIntegerField(verbose_name='Nombre de chambres')),
                ('energy_consumption', models.CharField(blank=True, max_length=1, null=True, verbose_name='Consommation \xe9nerg\xe9tique (kWhEP/m\xb2.an)', choices=[(b'A', 'A - \u2264 50'), (b'B', 'B - 51 \xe0 90'), (b'C', 'C - 91 \xe0 150'), (b'D', 'D - 151 \xe0 230'), (b'E', 'E - 231 \xe0 330'), (b'F', 'F - 331 \xe0 450'), (b'G', 'G - > 450')])),
                ('ad_valorem_tax', models.IntegerField(help_text='Montant annuel, sans espace, sans virgule', null=True, verbose_name='Taxe fonci\xe8re', blank=True)),
                ('housing_tax', models.IntegerField(help_text='Montant annuel, sans espace, sans virgule', null=True, verbose_name="Taxe d'habitation", blank=True)),
                ('maintenance_charges', models.IntegerField(help_text='Montant mensuel, sans espace, sans virgule', null=True, verbose_name='Charges', blank=True)),
                ('emission_of_greenhouse_gases', models.CharField(blank=True, max_length=1, null=True, verbose_name='\xc9missions de gaz \xe0 effet de serre (kgeqCO2/m\xb2.an)', choices=[(b'A', 'A - \u2264 5'), (b'B', 'B - 6 \xe0 10'), (b'C', 'C - 11 \xe0 20'), (b'D', 'D - 21 \xe0 35'), (b'E', 'E - 36 \xe0 55'), (b'F', 'F - 56 \xe0 80'), (b'G', 'G - > 80')])),
                ('ground_surface', models.IntegerField(null=True, verbose_name='Surface du terrain', blank=True)),
                ('floor', models.PositiveIntegerField(null=True, verbose_name='Etage', blank=True)),
                ('ground_floor', models.BooleanField(verbose_name='Rez de chauss\xe9')),
                ('top_floor', models.BooleanField(verbose_name='Dernier \xe9tage')),
                ('not_overlooked', models.BooleanField(verbose_name='Sans vis-\xe0-vis')),
                ('elevator', models.BooleanField(verbose_name='Ascenceur')),
                ('intercom', models.BooleanField(verbose_name='Interphone')),
                ('digicode', models.BooleanField(verbose_name='Digicode')),
                ('doorman', models.BooleanField(verbose_name='Gardien')),
                ('heating', models.CharField(blank=True, max_length=2, null=True, verbose_name='Chauffage', choices=[(b'1', 'individuel gaz'), (b'2', 'individuel \xe9lectrique'), (b'3', 'collectif gaz'), (b'4', 'collectif fuel'), (b'5', 'collectif r\xe9seau de chaleur'), (b'13', 'autres')])),
                ('kitchen', models.BooleanField(verbose_name='Cuisine \xe9quip\xe9e')),
                ('duplex', models.BooleanField(verbose_name='Duplex')),
                ('swimming_pool', models.BooleanField(verbose_name='Piscine')),
                ('alarm', models.BooleanField(verbose_name='Alarme')),
                ('air_conditioning', models.BooleanField(verbose_name='Climatisation')),
                ('fireplace', models.CharField(blank=True, max_length=2, null=True, verbose_name='Chemin\xe9e', choices=[(b'1', 'Foyer ouvert'), (b'2', 'Insert')])),
                ('terrace', models.IntegerField(null=True, verbose_name='Terrasse', blank=True)),
                ('balcony', models.IntegerField(null=True, verbose_name='Balcon', blank=True)),
                ('separate_dining_room', models.BooleanField(verbose_name='Cuisine s\xe9par\xe9e')),
                ('separate_toilet', models.IntegerField(null=True, verbose_name='Toilettes s\xe9par\xe9s', blank=True)),
                ('bathroom', models.IntegerField(null=True, verbose_name='Salle de bain', blank=True)),
                ('shower', models.IntegerField(null=True, verbose_name="Salle d'eau (douche)", blank=True)),
                ('separate_entrance', models.BooleanField(verbose_name='Entr\xe9e s\xe9par\xe9e')),
                ('cellar', models.BooleanField(verbose_name='Cave')),
                ('parking', models.CharField(blank=True, max_length=2, null=True, verbose_name='Parking', choices=[(b'1', 'Place de parking'), (b'2', 'Box ferm\xe9')])),
                ('orientation', models.CharField(max_length=255, null=True, verbose_name='Orientation', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'pictures/%Y/%m/%d', verbose_name=b'Photo')),
                ('title', models.CharField(max_length=255, null=True, verbose_name=b'Titre', blank=True)),
                ('ad', models.ForeignKey(to='ads.Ad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdSearchRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('ad_notified', models.DateTimeField(null=True, blank=True)),
                ('search_notified', models.DateTimeField(null=True, blank=True)),
                ('ad_contacted', models.DateTimeField(null=True, blank=True)),
                ('search_contacted', models.DateTimeField(null=True, blank=True)),
                ('valid', models.BooleanField()),
                ('ad', models.ForeignKey(to='ads.Ad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HabitationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'slug_format', verbose_name='slug', editable=False, blank=True)),
                ('location', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='Localisation')),
                ('price_max', models.PositiveIntegerField(verbose_name='Prix max')),
                ('surface_min', models.PositiveIntegerField(verbose_name='Surface min')),
                ('habitation_types', models.ManyToManyField(to=b'ads.HabitationType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='adsearchrelation',
            name='search',
            field=models.ForeignKey(to='ads.Search'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='adsearchrelation',
            unique_together=set([('ad', 'search')]),
        ),
        migrations.AddField(
            model_name='ad',
            name='habitation_type',
            field=models.ForeignKey(verbose_name=b'Type de bien', to='ads.HabitationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='air_conditioning',
            field=models.BooleanField(default=False, verbose_name='Climatisation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='alarm',
            field=models.BooleanField(default=False, verbose_name='Alarme'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='cellar',
            field=models.BooleanField(default=False, verbose_name='Cave'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='digicode',
            field=models.BooleanField(default=False, verbose_name='Digicode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='doorman',
            field=models.BooleanField(default=False, verbose_name='Gardien'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='duplex',
            field=models.BooleanField(default=False, verbose_name='Duplex'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='elevator',
            field=models.BooleanField(default=False, verbose_name='Ascenceur'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='ground_floor',
            field=models.BooleanField(default=False, verbose_name='Rez de chauss\xe9'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='intercom',
            field=models.BooleanField(default=False, verbose_name='Interphone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='kitchen',
            field=models.BooleanField(default=False, verbose_name='Cuisine \xe9quip\xe9e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='not_overlooked',
            field=models.BooleanField(default=False, verbose_name='Sans vis-\xe0-vis'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='separate_dining_room',
            field=models.BooleanField(default=False, verbose_name='Cuisine s\xe9par\xe9e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='separate_entrance',
            field=models.BooleanField(default=False, verbose_name='Entr\xe9e s\xe9par\xe9e'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='swimming_pool',
            field=models.BooleanField(default=False, verbose_name='Piscine'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ad',
            name='top_floor',
            field=models.BooleanField(default=False, verbose_name='Dernier \xe9tage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adsearchrelation',
            name='valid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        # migrations.AlterField(
        #     model_name='ad',
        #     name='location',
        #     field=django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Localisation'),
        #     preserve_default=True,
        # ),
        # migrations.AlterField(
        #     model_name='search',
        #     name='location',
        #     field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='Localisation'),
        #     preserve_default=True,
        # ),
        migrations.AlterField(
            model_name='search',
            name='price_max',
            field=models.PositiveIntegerField(verbose_name='Prix maximum'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='surface_min',
            field=models.PositiveIntegerField(verbose_name='Surface minimale'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='rooms_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Nombre de pi\xe8ces minimum', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='air_conditioning',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Climatisation', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='alarm',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Alarme', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='balcony',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Balcon', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='bathroom',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Salle de bain', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='bedrooms_min',
            field=models.PositiveIntegerField(null=True, verbose_name='Nombre de chambres minimum', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='cellar',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Cave', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='digicode',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Digicode', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='doorman',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Gardien', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='duplex',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Duplex', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='elevator',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Ascenceur', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='fireplace',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Chemin\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='ground_floor',
            field=ads.models.search.IndifferentBooleanField(default=None, verbose_name='Rez de chauss\xe9', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='ground_surface_min',
            field=models.IntegerField(null=True, verbose_name='Surface du terrain minimale', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='intercom',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Interphone', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='kitchen',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Cuisine \xe9quip\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='not_overlooked',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Sans vis-\xe0-vis', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='parking',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Parking', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='separate_dining_room',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Cuisine s\xe9par\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='separate_entrance',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Entr\xe9e s\xe9par\xe9e', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='separate_toilet',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Toilettes s\xe9par\xe9s', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='shower',
            field=ads.models.search.IndifferentBooleanField(verbose_name="Salle d'eau (douche)", choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='swimming_pool',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Piscine', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='terrace',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Terrasse', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='top_floor',
            field=ads.models.search.IndifferentBooleanField(verbose_name='Dernier \xe9tage', choices=[(None, 'Indiff\xe9rent'), (True, 'Oui'), (False, 'Non')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ad',
            name='transaction',
            field=models.CharField(default='sale', max_length=4, choices=[(b'sale', 'Vente'), (b'rent', 'Location')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='search',
            name='transaction',
            field=models.CharField(default='sale', max_length=4, choices=[(b'sale', 'Vente'), (b'rent', 'Location')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='search',
            name='habitation_types',
            field=models.ManyToManyField(to=b'ads.HabitationType', verbose_name="Types d'habitations"),
            preserve_default=True,
        ),
        migrations.RunPython(create_habitation_types),
        migrations.RunPython(fill_flatpages),
    ]
