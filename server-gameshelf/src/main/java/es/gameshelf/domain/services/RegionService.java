package es.gameshelf.domain.services;

import es.gameshelf.domain.Region;
import es.gameshelf.domain.interfaces.repository.IRegionRepository;
import es.gameshelf.domain.interfaces.service.IRegionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class RegionService implements IRegionService {
    /**
     * Properties
     */
    IRegionRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IRegionRepository repository) {
        this.repository = repository;
    }

    @Override
    public Region add(String name, String initials) {
        Region item = new Region();
        item.setName(name);
        item.setAdditionalText(initials);

        return repository.save(item);
    }

    @Override
    public List<Region> findAll() {
        return repository.findAll();
    }

    @Override
    public Region findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Region findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Region update(Integer id, String name, String initials) {
        Region item = new Region(id);
        item.setName(name);
        item.setAdditionalText(initials);
        return null;
    }
}
