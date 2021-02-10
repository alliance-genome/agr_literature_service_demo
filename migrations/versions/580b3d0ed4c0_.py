"""empty message

Revision ID: 580b3d0ed4c0
Revises: b05a374609ad
Create Date: 2021-02-06 18:47:09.156738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '580b3d0ed4c0'
down_revision = 'b05a374609ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reference',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('primaryId', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('datePublished', sa.String(length=255), nullable=True),
    sa.Column('dateArrivedInPubMed', sa.String(length=255), nullable=True),
    sa.Column('dateLastModified', sa.String(length=255), nullable=True),
    sa.Column('volume', sa.String(length=255), nullable=True),
    sa.Column('abstract', sa.String(length=255), nullable=True),
    sa.Column('citation', sa.String(length=255), nullable=True),
    sa.Column('pubMedType', sa.String(length=255), nullable=True),
    sa.Column('publisher', sa.String(length=255), nullable=True),
    sa.Column('allianceCategory', sa.Enum('Research_Article', 'Review_Article', 'Thesis', 'Book', 'Other', 'Preprint', 'Conference_Publication', 'Personal_Communication', 'Direct_Data_Submission', 'Internal_Process_Reference', 'Unknown', 'Retraction', name='alliancecategory'), nullable=True),
    sa.Column('issueName', sa.String(length=255), nullable=True),
    sa.Column('issueDate', sa.String(length=255), nullable=True),
    sa.Column('resourceAbbreviation', sa.String(length=255), nullable=True),
    sa.Column('updatedBy', sa.String(length=255), nullable=True),
    sa.Column('dateUpdated', sa.DateTime(), nullable=False),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('primaryId')
    )
    op.create_table('resource',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('primaryId', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('isoAbbreviation', sa.String(length=255), nullable=True),
    sa.Column('medlineAbbreviation', sa.String(length=255), nullable=True),
    sa.Column('copyrightDate', sa.DateTime(), nullable=True),
    sa.Column('publisher', sa.String(length=255), nullable=True),
    sa.Column('printISSN', sa.String(length=255), nullable=True),
    sa.Column('onlineISSN', sa.String(length=255), nullable=True),
    sa.Column('pages', sa.Integer(), nullable=True),
    sa.Column('abstract', sa.String(length=255), nullable=True),
    sa.Column('summary', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('firstName', sa.String(length=255), nullable=True),
    sa.Column('lastName', sa.String(length=255), nullable=True),
    sa.Column('valid', sa.Boolean(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('string', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mesh_term',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('meshHeadingTerm', sa.String(length=255), nullable=True),
    sa.Column('meshQualifierTerm', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mod_reference_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('referenceType', sa.String(length=255), nullable=True),
    sa.Column('source', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('page',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('string', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pubmed',
    sa.Column('id', sa.String(length=10), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pubmod',
    sa.Column('id', sa.String(length=10), nullable=False),
    sa.Column('mod', sa.String(length=20), nullable=True),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resource_author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sourceId', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('firstName', sa.String(length=255), nullable=True),
    sa.Column('lastName', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['sourceId'], ['resource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resource_editor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sourceId', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('firstName', sa.String(length=255), nullable=True),
    sa.Column('lastName', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['sourceId'], ['resource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resource_title_synonym',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resourceId', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['resourceId'], ['resource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resource_volume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('volume', sa.String(length=255), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['resource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referenceId', sa.Integer(), nullable=False),
    sa.Column('tagName', sa.Enum('canShowImages', 'PMCOpenAccess', 'inCorpus', 'notRelevant', name='tagname'), nullable=False),
    sa.Column('tagSource', sa.Enum('SGD', 'ZFIN', 'RGD', 'WB', 'MGI', 'FB', name='tagsource'), nullable=False),
    sa.Column('dateCreated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['referenceId'], ['reference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag')
    op.drop_table('resource_volume')
    op.drop_table('resource_title_synonym')
    op.drop_table('resource_editor')
    op.drop_table('resource_author')
    op.drop_table('pubmod')
    op.drop_table('pubmed')
    op.drop_table('page')
    op.drop_table('mod_reference_type')
    op.drop_table('mesh_term')
    op.drop_table('keyword')
    op.drop_table('author')
    op.drop_table('resource')
    op.drop_table('reference')
    # ### end Alembic commands ###